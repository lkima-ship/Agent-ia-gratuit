cat > src/modules/outlook_client.py << 'EOF'
"""
Client Outlook pour l'agent IA
Version sécurisée pour iOS/a-Shell
"""

import imaplib
import email
from email.header import decode_header
import ssl
from typing import List, Dict, Any, Optional

class OutlookClient:
    """Client sécurisé pour Outlook"""
    
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.server = "outlook.office365.com"
        self.port = 993
        self.imap = None
        
    def connect(self) -> bool:
        """Établir une connexion sécurisée"""
        try:
            context = ssl.create_default_context()
            self.imap = imaplib.IMAP4_SSL(
                self.server,
                self.port,
                ssl_context=context
            )
            self.imap.login(self.email_address, self.password)
            self.imap.select("INBOX")
            return True
        except Exception as e:
            print(f"❌ Erreur de connexion: {e}")
            return False
    
    def get_unread_count(self) -> int:
        """Compter les emails non lus"""
        if not self.imap:
            return 0
        try:
            status, messages = self.imap.search(None, 'UNSEEN')
            if status == 'OK':
                return len(messages[0].split())
        except:
            pass
        return 0
    
    def disconnect(self):
        """Fermer la connexion"""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass

if __name__ == "__main__":
    import os
    from config.settings import config
    
    print("🧪 Test du client Outlook")
    if not config.EMAIL_ADDRESS or not config.EMAIL_PASSWORD:
        print("⚠️  Configuration email manquante dans .env")
    else:
        client = OutlookClient(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        if client.connect():
            print("✅ Connecté à Outlook")
            count = client.get_unread_count()
            print(f"📬 Emails non lus: {count}")
            client.disconnect()
        else:
            print("❌ Échec de connexion")
EOF
