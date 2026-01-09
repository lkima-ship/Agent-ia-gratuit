import email
from email.header import decode_header
import imaplib
from typing import List, Dict, Any
from loguru import logger
import time

class EmailProcessor:
    """Processeur d'emails basique avec IMAP"""
    
    def __init__(self, imap_server: str = "imap.gmail.com", port: int = 993):
        self.imap_server = imap_server
        self.port = port
        self.connection = None
        self.logger = logger.bind(module="EmailProcessor")
    
    def connect(self, username: str, password: str) -> bool:
        """Connexion au serveur IMAP"""
        try:
            self.logger.info(f"Connexion à {self.imap_server}:{self.port}")
            self.connection = imaplib.IMAP4_SSL(self.imap_server, self.port)
            self.connection.login(username, password)
            self.connection.select("INBOX")
            self.logger.success("Connexion IMAP réussie")
            return True
        except Exception as e:
            self.logger.error(f"Erreur de connexion: {e}")
            return False
    
    def decode_mime_words(self, text: str) -> str:
        """Décodage des en-têtes MIME"""
        if text is None:
            return ""
        
        decoded_words = []
        for word, encoding in decode_header(text):
            if isinstance(word, bytes):
                try:
                    word = word.decode(encoding if encoding else 'utf-8')
                except:
                    word = word.decode('utf-8', errors='ignore')
            decoded_words.append(str(word))
        return ' '.join(decoded_words)
    
    def fetch_unread_emails(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupération des emails non lus"""
        if not self.connection:
            self.logger.warning("Non connecté au serveur IMAP")
            return []
        
        try:
            # Rechercher les emails non lus
            self.connection.select("INBOX")
            status, messages = self.connection.search(None, 'UNSEEN')
            
            if status != "OK":
                self.logger.warning("Aucun email non lu trouvé")
                return []
            
            email_ids = messages[0].split()
            emails = []
            
            # Limiter le nombre d'emails
            email_ids = email_ids[-limit:] if limit else email_ids
            
            self.logger.info(f"Récupération de {len(email_ids)} email(s)")
            
            for email_id in email_ids:
                try:
                    # Récupérer l'email
                    status, msg_data = self.connection.fetch(email_id, '(RFC822)')
                    
                    if status != "OK":
                        continue
                    
                    # Parser l'email
                    raw_email = msg_data[0][1]
                    email_message = email.message_from_bytes(raw_email)
                    
                    # Extraire les informations
                    subject = self.decode_mime_words(email_message.get("Subject", ""))
                    from_ = self.decode_mime_words(email_message.get("From", ""))
                    date = email_message.get("Date", "")
                    
                    # Extraire le corps
                    body = ""
                    if email_message.is_multipart():
                        for part in email_message.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            # Ignorer les pièces jointes
                            if "attachment" in content_disposition:
                                continue
                            
                            if content_type == "text/plain":
                                try:
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        # Email non multipart
                        try:
                            body = email_message.get_payload(decode=True).decode()
                        except:
                            body = email_message.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
                    email_data = {
                        "id": email_id.decode(),
                        "subject": subject,
                        "from": from_,
                        "date": date,
                        "body": body[:1000],  # Limiter la taille
                        "full_body": body,
                        "is_read": False
                    }
                    
                    emails.append(email_data)
                    self.logger.debug(f"Email récupéré: {subject}")
                    
                except Exception as e:
                    self.logger.error(f"Erreur traitement email {email_id}: {e}")
                    continue
            
            return emails
            
        except Exception as e:
            self.logger.error(f"Erreur récupération emails: {e}")
            return []
    
    def mark_as_read(self, email_id: str) -> bool:
        """Marquer un email comme lu"""
        try:
            self.connection.store(email_id, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            self.logger.error(f"Erreur marquage comme lu: {e}")
            return False
    
    def disconnect(self):
        """Déconnexion propre"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
                self.logger.info("Déconnexion IMAP réussie")
            except:
                pass
