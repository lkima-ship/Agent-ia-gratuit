# Ajouter en début de fichier
import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db_file = "agent_data.db"
        self.init_database()
    
    def init_database(self):
        """Initialiser la base de données"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Table emails
        c.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sujet TEXT NOT NULL,
                expediteur TEXT NOT NULL,
                contenu TEXT,
                date TEXT NOT NULL,
                traite INTEGER DEFAULT 0
            )
        ''')
        
        # Table rendez-vous
        c.execute('''
            CREATE TABLE IF NOT EXISTS rendezvous (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                date TEXT NOT NULL,
                heure TEXT NOT NULL,
                lieu TEXT,
                participant TEXT,
                statut TEXT DEFAULT 'planifié'
            )
        ''')
        
        # Table statistiques
        c.execute('''
            CREATE TABLE IF NOT EXISTS statistiques (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_action TEXT NOT NULL,
                date_action TEXT NOT NULL,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Base de données initialisée")
    
    def ajouter_email(self, sujet, expediteur, contenu=""):
        """Ajouter un email à la base"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        c.execute(
            "INSERT INTO emails (sujet, expediteur, contenu, date) VALUES (?, ?, ?, ?)",
            (sujet, expediteur, contenu, date)
        )
        
        # Enregistrer dans les statistiques
        c.execute(
            "INSERT INTO statistiques (type_action, date_action, details) VALUES (?, ?, ?)",
            ("email_ajoute", date, f"Sujet: {sujet}")
        )
        
        conn.commit()
        conn.close()
        return True
    
    def ajouter_rendezvous(self, titre, date, heure, lieu="", participant=""):
        """Ajouter un rendez-vous"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute(
            "INSERT INTO rendezvous (titre, date, heure, lieu, participant) VALUES (?, ?, ?, ?, ?)",
            (titre, date, heure, lieu, participant)
        )
        
        # Statistiques
        date_action = datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute(
            "INSERT INTO statistiques (type_action, date_action, details) VALUES (?, ?, ?)",
            ("rdv_ajoute", date_action, f"Titre: {titre}")
        )
        
        conn.commit()
        conn.close()
        return True
    
    def get_stats(self):
        """Obtenir les statistiques"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        # Compter les emails
        c.execute("SELECT COUNT(*) FROM emails")
        emails = c.fetchone()[0]
        
        # Compter les rendez-vous
        c.execute("SELECT COUNT(*) FROM rendezvous")
        rdv = c.fetchone()[0]
        
        # Compter les notes (si table existe)
        try:
            c.execute("SELECT COUNT(*) FROM notes_vocales")
            notes = c.fetchone()[0]
        except:
            notes = 0
        
        conn.close()
        
        return {
            "emails": emails,
            "rendezvous": rdv,
            "notes": notes
        }
    
    def detail_rendezvous(self):
        """Afficher les détails des rendez-vous"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute("SELECT * FROM rendezvous ORDER BY date, heure")
        rdvs = c.fetchall()
        
        if not rdvs:
            print("Aucun rendez-vous trouvé.")
            conn.close()
            return
        
        print("\n" + "="*60)
        print("📅 DÉTAILS DES RENDEZ-VOUS")
        print("="*60)
        
        for rdv in rdvs:
            id_rdv, titre, date, heure, lieu, participant, statut = rdv
            print(f"\n🔹 RENDEZ-VOUS #{id_rdv}")
            print(f"   Titre: {titre}")
            print(f"   Date: {date}")
            print(f"   Heure: {heure}")
            print(f"   Lieu: {lieu}")
            print(f"   Participant: {participant}")
            print(f"   Statut: {statut}")
        
        print("="*60)
        conn.close()
    
    def rechercher_emails(self, mot_cle):
        """Rechercher des emails par mot-clé"""
        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        
        c.execute(
            "SELECT * FROM emails WHERE sujet LIKE ? OR expediteur LIKE ? OR contenu LIKE ?",
            (f'%{mot_cle}%', f'%{mot_cle}%', f'%{mot_cle}%')
        )
        
        resultats = c.fetchall()
        
        if not resultats:
            print(f"Aucun email trouvé avec le mot-clé '{mot_cle}'")
            conn.close()
            return
        
        print(f"\n🔍 RÉSULTATS DE RECHERCHE : '{mot_cle}'")
        print("="*60)
        
        for email in resultats:
            id_email, sujet, expediteur, contenu, date, traite = email
            statut = "✅ Traité" if traite else "📧 Non traité"
            print(f"\nID: {id_email} | {statut}")
            print(f"Expéditeur: {expediteur}")
            print(f"Sujet: {sujet}")
            print(f"Date: {date}")
            if contenu:
                preview = contenu[:100] + "..." if len(contenu) > 100 else contenu
                print(f"Contenu: {preview}")
        
        print("="*60)
        conn.close()

# Ajouter cette fonction pour étendre les commandes
def executer_commande(commande, db):
    """Exécuter une commande avancée"""
    commande = commande.lower().strip()
    
    if commande == "detail rdv" or commande == "details rdv":
        db.detail_rendezvous()
    
    elif commande.startswith("rechercher "):
        mot_cle = commande.split(" ", 1)[1]
        db.rechercher_emails(mot_cle)
    
    elif commande == "aide" or commande == "help":
        print("\n📚 COMMANDES DISPONIBLES :")
        print("  detail rdv        - Afficher les détails des rendez-vous")
        print("  rechercher [mot]  - Rechercher dans les emails")
        print("  stats détaillées  - Statistiques avancées")
        print("  ajouter email     - Ajouter un nouvel email")
        print("  ajouter rdv       - Ajouter un nouveau rendez-vous")
        print("  aide              - Afficher cette aide")
        print("  quit              - Quitter")
    
    elif commande == "stats détaillées":
        stats = db.get_stats()
        print("\n📊 STATISTIQUES DÉTAILLÉES :")
        print(f"  📧 Emails totaux: {stats['emails']}")
        print(f"  📅 Rendez-vous: {stats['rendezvous']}")
        print(f"  🎤 Notes vocales: {stats['notes']}")
        
        # Calculer les tendances
        conn = sqlite3.connect(db.db_file)
        c = conn.cursor()
        
        # Emails des derniers jours
        c.execute("SELECT COUNT(*) FROM emails WHERE date >= datetime('now', '-7 days')")
        emails_7j = c.fetchone()[0]
        print(f"  📈 Emails (7j): {emails_7j}")
        
        # RDV à venir
        aujourdhui = datetime.now().strftime("%Y-%m-%d")
        c.execute("SELECT COUNT(*) FROM rendezvous WHERE date >= ?", (aujourdhui,))
        rdv_futurs = c.fetchone()[0]
        print(f"  🗓️  RDV à venir: {rdv_futurs}")
        
        conn.close()
    
    elif commande == "ajouter email":
        print("\n📝 AJOUTER UN EMAIL :")
        sujet = input("Sujet: ")
        expediteur = input("Expéditeur: ")
        contenu = input("Contenu (optionnel): ")
        
        if db.ajouter_email(sujet, expediteur, contenu):
            print("✅ Email ajouté avec succès!")
    
    elif commande == "ajouter rdv":
        print("\n📅 AJOUTER UN RENDEZ-VOUS :")
        titre = input("Titre: ")
        date = input("Date (AAAA-MM-JJ): ")
        heure = input("Heure (HH:MM): ")
        lieu = input("Lieu (optionnel): ")
        participant = input("Participant (optionnel): ")
        
        if db.ajouter_rendezvous(titre, date, heure, lieu, participant):
            print("✅ Rendez-vous ajouté avec succès!")
    
    elif commande == "quit" or commande == "exit":
        print("👋 Au revoir!")
        exit(0)
    
    else:
        print(f"❌ Commande non reconnue: {commande}")
        print("Tapez 'aide' pour voir les commandes disponibles.")
#!/usr/bin/env python3
# agent_ia_complet.py - Agent IA avec toutes les fonctionnalités

import os
import sys
import json
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class AgentIAGratuit:
    def __init__(self):
        self.version = "2.0.0"
        self.auteur = "Votre Nom"
        self.db_file = "agent_ia.db"
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        # Couleurs pour le terminal
        self.COLORS = {
            'RESET': '\033[0m',
            'ROUGE': '\033[91m',
            'VERT': '\033[92m',
            'JAUNE': '\033[93m',
            'BLEU': '\033[94m',
            'VIOLET': '\033[95m',
            'CYAN': '\033[96m',
        }
        
        self.init_database()
        self.charger_donnees()
        
    def init_database(self):
        """Initialiser la base de données SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            
            # Table des emails
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sujet TEXT NOT NULL,
                    expediteur TEXT NOT NULL,
                    contenu TEXT,
                    date TEXT NOT NULL,
                    priorite INTEGER DEFAULT 1,
                    categorie TEXT DEFAULT 'inbox',
                    traite BOOLEAN DEFAULT 0,
                    lu BOOLEAN DEFAULT 0
                )
            ''')
            
            # Table des rendez-vous
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS rendezvous (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titre TEXT NOT NULL,
                    description TEXT,
                    date TEXT NOT NULL,
                    heure TEXT NOT NULL,
                    duree INTEGER DEFAULT 60,
                    participants TEXT,
                    lieu TEXT,
                    statut TEXT DEFAULT 'planifié',
                    rappel INTEGER DEFAULT 15,
                    couleur TEXT DEFAULT '#3498db'
                )
            ''')
            
            # Table des notes vocales
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS notes_vocales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom_fichier TEXT,
                    transcription TEXT,
                    duree INTEGER,
                    date TEXT NOT NULL,
                    tags TEXT,
                    important BOOLEAN DEFAULT 0
                )
            ''')
            
            # Table des statistiques
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS statistiques (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    action TEXT NOT NULL,
                    details TEXT
                )
            ''')
            
            self.conn.commit()
            print(f"{self.COLORS['VERT']}✅ Base de données initialisée{self.COLORS['RESET']}")
            
        except Exception as e:
            print(f"{self.COLORS['ROUGE']}❌ Erreur base de données: {e}{self.COLORS['RESET']}")
            sys.exit(1)
    
    def charger_donnees(self):
        """Charger les données de démo si la base est vide"""
        # Vérifier si la base est vide
        self.cursor.execute("SELECT COUNT(*) FROM emails")
        if self.cursor.fetchone()[0] == 0:
            self.ajouter_donnees_demo()
    
    def ajouter_donnees_demo(self):
        """Ajouter des données de démonstration"""
        # Emails de démo
        emails_demo = [
            ("Réunion projet", "boss@entreprise.com", "Bonjour, réunion demain à 10h.", "2024-01-15 09:30"),
            ("Facture", "compta@fournisseur.fr", "Votre facture n°12345", "2024-01-14 14:20"),
            ("Newsletter", "news@tech.com", "Les dernières nouvelles tech...", "2024-01-13 11:15"),
        ]
        
        for sujet, expediteur, contenu, date in emails_demo:
            self.cursor.execute(
                "INSERT INTO emails (sujet, expediteur, contenu, date) VALUES (?, ?, ?, ?)",
                (sujet, expediteur, contenu, date)
            )
        
        # Rendez-vous de démo
        rdv_demo = [
            ("Réunion équipe", "Point sur le projet X", "2024-01-16", "10:00", "Salle A"),
            ("Dentiste", "Contrôle annuel", "2024-01-18", "14:30", "Dr. Dupont"),
            ("Déjeuner client", "Présentation produit", "2024-01-20", "12:30", "Restaurant Le Central"),
        ]
        
        for titre, description, date, heure, lieu in rdv_demo:
            self.cursor.execute(
                "INSERT INTO rendezvous (titre, description, date, heure, lieu) VALUES (?, ?, ?, ?, ?)",
                (titre, description, date, heure, lieu)
            )
        
        self.conn.commit()
        print(f"{self.COLORS['VERT']}✅ Données de démonstration ajoutées{self.COLORS['RESET']}")
    
    def afficher_menu(self):
        """Afficher le menu principal"""
        while True:
            self.clear_screen()
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['VIOLET']}🤖 AGENT IA GRATUIT - v{self.version}{self.COLORS['RESET']}")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}📊 STATS RAPIDES:{self.COLORS['RESET']}")
            self.afficher_stats_rapides()
            print(f"{self.COLORS['CYAN']}{'-'*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['BLEU']}1.{self.COLORS['RESET']} 📧 Gérer les emails")
            print(f"{self.COLORS['BLEU']}2.{self.COLORS['RESET']} 📅 Gérer les rendez-vous")
            print(f"{self.COLORS['BLEU']}3.{self.COLORS['RESET']} 🎤 Gérer les notes vocales")
            print(f"{self.COLORS['BLEU']}4.{self.COLORS['RESET']} 📊 Statistiques détaillées")
            print(f"{self.COLORS['BLEU']}5.{self.COLORS['RESET']} 🔍 Recherche intelligente")
            print(f"{self.COLORS['BLEU']}6.{self.COLORS['RESET']} ⚙️  Paramètres")
            print(f"{self.COLORS['BLEU']}7.{self.COLORS['RESET']} ℹ️  Aide")
            print(f"{self.COLORS['BLEU']}0.{self.COLORS['RESET']} 🚪 Quitter")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            choix = input(f"\n{self.COLORS['VERT']}Votre choix (0-7): {self.COLORS['RESET']}").strip()
            
            if choix == "1":
                self.menu_emails()
            elif choix == "2":
                self.menu_rendezvous()
            elif choix == "3":
                self.menu_notes_vocales()
            elif choix == "4":
                self.menu_statistiques()
            elif choix == "5":
                self.menu_recherche()
            elif choix == "6":
                self.menu_parametres()
            elif choix == "7":
                self.afficher_aide()
            elif choix == "0":
                print(f"{self.COLORS['JAUNE']}👋 Au revoir!{self.COLORS['RESET']}")
                self.conn.close()
                sys.exit(0)
            else:
                print(f"{self.COLORS['ROUGE']}❌ Choix invalide!{self.COLORS['RESET']}")
                input("Appuyez sur Entrée pour continuer...")
    
    def afficher_stats_rapides(self):
        """Afficher les statistiques rapides"""
        try:
            # Compter les emails non lus
            self.cursor.execute("SELECT COUNT(*) FROM emails WHERE lu = 0")
            emails_non_lus = self.cursor.fetchone()[0]
            
            # Compter les rendez-vous d'aujourd'hui
            aujourdhui = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("SELECT COUNT(*) FROM rendezvous WHERE date = ?", (aujourdhui,))
            rdv_aujourdhui = self.cursor.fetchone()[0]
            
            # Dernière note vocale
            self.cursor.execute("SELECT COUNT(*) FROM notes_vocales")
            total_notes = self.cursor.fetchone()[0]
            
            print(f"  📧 Emails non lus: {emails_non_lus}")
            print(f"  📅 RDV aujourd'hui: {rdv_aujourdhui}")
            print(f"  🎤 Notes vocales: {total_notes}")
            
        except Exception as e:
            print(f"  ⚠️  Erreur stats: {e}")
    
    def menu_emails(self):
        """Menu de gestion des emails"""
        while True:
            self.clear_screen()
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['VERT']}📧 GESTION DES EMAILS{self.COLORS['RESET']}")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            self.cursor.execute("""
                SELECT id, sujet, expediteur, date, lu 
                FROM emails 
                ORDER BY date DESC 
                LIMIT 10
            """)
            emails = self.cursor.fetchall()
            
            if emails:
                for email in emails:
                    id_email, sujet, expediteur, date, lu = email
                    statut = "📬" if not lu else "📭"
                    print(f"{statut} {id_email:3d} | {sujet[:30]:30} | {expediteur[:20]:20} | {date}")
            else:
                print("Aucun email")
            
            print(f"\n{self.COLORS['CYAN']}{'-'*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}Commandes:{self.COLORS['RESET']}")
            print("  ajouter  - Ajouter un email")
            print("  voir [id] - Voir un email")
            print("  supp [id] - Supprimer un email")
            print("  marquer [id] - Marquer comme lu/non lu")
            print("  rechercher [mot] - Rechercher")
            print("  retour  - Retour au menu")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            commande = input(f"\n{self.COLORS['VERT']}email> {self.COLORS['RESET']}").strip().lower()
            
            if commande == "retour":
                break
            elif commande.startswith("ajouter"):
                self.ajouter_email()
            elif commande.startswith("voir "):
                try:
                    id_email = int(commande.split()[1])
                    self.voir_email(id_email)
                except:
                    print(f"{self.COLORS['ROUGE']}❌ ID invalide{self.COLORS['RESET']}")
            elif commande.startswith("supp "):
                try:
                    id_email = int(commande.split()[1])
                    self.supprimer_email(id_email)
                except:
                    print(f"{self.COLORS['ROUGE']}❌ ID invalide{self.COLORS['RESET']}")
            elif commande.startswith("marquer "):
                try:
                    id_email = int(commande.split()[1])
                    self.marquer_email(id_email)
                except:
                    print(f"{self.COLORS['ROUGE']}❌ ID invalide{self.COLORS['RESET']}")
            elif commande.startswith("rechercher "):
                mot = commande.split(" ", 1)[1]
                self.rechercher_emails(mot)
            else:
                print(f"{self.COLORS['ROUGE']}❌ Commande inconnue{self.COLORS['RESET']}")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def ajouter_email(self):
        """Ajouter un nouvel email"""
        print(f"\n{self.COLORS['VERT']}📝 NOUVEL EMAIL:{self.COLORS['RESET']}")
        sujet = input("Sujet: ")
        expediteur = input("Expéditeur: ")
        contenu = input("Contenu (multiligne, finir par une ligne vide):\n")
        lignes = []
        while True:
            ligne = input()
            if ligne == "":
                break
            lignes.append(ligne)
        contenu = "\n".join(lignes)
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.cursor.execute(
            "INSERT INTO emails (sujet, expediteur, contenu, date) VALUES (?, ?, ?, ?)",
            (sujet, expediteur, contenu, date)
        )
        self.conn.commit()
        print(f"{self.COLORS['VERT']}✅ Email ajouté!{self.COLORS['RESET']}")
    
    def menu_rendezvous(self):
        """Menu de gestion des rendez-vous"""
        while True:
            self.clear_screen()
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['VERT']}📅 GESTION DES RENDEZ-VOUS{self.COLORS['RESET']}")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            # Afficher les rendez-vous à venir
            aujourdhui = datetime.now().strftime("%Y-%m-%d")
            self.cursor.execute("""
                SELECT id, titre, date, heure, lieu, statut 
                FROM rendezvous 
                WHERE date >= ?
                ORDER BY date, heure
                LIMIT 10
            """, (aujourdhui,))
            
            rdvs = self.cursor.fetchall()
            
            if rdvs:
                for rdv in rdvs:
                    id_rdv, titre, date, heure, lieu, statut = rdv
                    print(f"📅 {id_rdv:3d} | {titre[:25]:25} | {date} {heure} | {lieu[:15]:15} | {statut}")
            else:
                print("Aucun rendez-vous à venir")
            
            print(f"\n{self.COLORS['CYAN']}{'-'*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}Commandes:{self.COLORS['RESET']}")
            print("  ajouter  - Ajouter un rendez-vous")
            print("  aujourdhui - Voir les RDV d'aujourd'hui")
            print("  semaine  - Voir les RDV de la semaine")
            print("  detail [id] - Voir détail")
            print("  supp [id] - Supprimer")
            print("  retour  - Retour au menu")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            commande = input(f"\n{self.COLORS['VERT']}rdv> {self.COLORS['RESET']}").strip().lower()
            
            if commande == "retour":
                break
            elif commande == "ajouter":
                self.ajouter_rendezvous()
            elif commande == "aujourdhui":
                self.afficher_rdv_aujourdhui()
            elif commande == "semaine":
                self.afficher_rdv_semaine()
            elif commande.startswith("detail "):
                try:
                    id_rdv = int(commande.split()[1])
                    self.detail_rendezvous(id_rdv)
                except:
                    print(f"{self.COLORS['ROUGE']}❌ ID invalide{self.COLORS['RESET']}")
            elif commande.startswith("supp "):
                try:
                    id_rdv = int(commande.split()[1])
                    self.supprimer_rendezvous(id_rdv)
                except:
                    print(f"{self.COLORS['ROUGE']}❌ ID invalide{self.COLORS['RESET']}")
            else:
                print(f"{self.COLORS['ROUGE']}❌ Commande inconnue{self.COLORS['RESET']}")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def ajouter_rendezvous(self):
        """Ajouter un nouveau rendez-vous"""
        print(f"\n{self.COLORS['VERT']}📝 NOUVEAU RENDEZ-VOUS:{self.COLORS['RESET']}")
        titre = input("Titre: ")
        description = input("Description: ")
        date = input("Date (YYYY-MM-DD): ")
        heure = input("Heure (HH:MM): ")
        duree = input("Durée (minutes, défaut 60): ") or "60"
        lieu = input("Lieu: ")
        participants = input("Participants (séparés par des virgules): ")
        
        try:
            self.cursor.execute("""
                INSERT INTO rendezvous 
                (titre, description, date, heure, duree, lieu, participants) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (titre, description, date, heure, duree, lieu, participants))
            self.conn.commit()
            print(f"{self.COLORS['VERT']}✅ Rendez-vous ajouté!{self.COLORS['RESET']}")
        except Exception as e:
            print(f"{self.COLORS['ROUGE']}❌ Erreur: {e}{self.COLORS['RESET']}")
    
    def menu_statistiques(self):
        """Menu des statistiques détaillées"""
        self.clear_screen()
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        print(f"{self.COLORS['VERT']}📊 STATISTIQUES DÉTAILLÉES{self.COLORS['RESET']}")
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        
        # Statistiques emails
        self.cursor.execute("SELECT COUNT(*) FROM emails")
        total_emails = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM emails WHERE lu = 0")
        emails_non_lus = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM emails WHERE traite = 1")
        emails_traites = self.cursor.fetchone()[0]
        
        # Statistiques rendez-vous
        self.cursor.execute("SELECT COUNT(*) FROM rendezvous")
        total_rdv = self.cursor.fetchone()[0]
        
        aujourdhui = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT COUNT(*) FROM rendezvous WHERE date >= ?", (aujourdhui,))
        rdv_futurs = self.cursor.fetchone()[0]
        
        # Statistiques notes
        self.cursor.execute("SELECT COUNT(*) FROM notes_vocales")
        total_notes = self.cursor.fetchone()[0]
        
        print(f"\n{self.COLORS['JAUNE']}📧 EMAILS:{self.COLORS['RESET']}")
        print(f"  Total: {total_emails}")
        print(f"  Non lus: {emails_non_lus}")
        print(f"  Traités: {emails_traites}")
        if total_emails > 0:
            taux = (emails_traites / total_emails) * 100
            print(f"  Taux de traitement: {taux:.1f}%")
        
        print(f"\n{self.COLORS['JAUNE']}📅 RENDEZ-VOUS:{self.COLORS['RESET']}")
        print(f"  Total: {total_rdv}")
        print(f"  À venir: {rdv_futurs}")
        print(f"  Passés: {total_rdv - rdv_futurs}")
        
        print(f"\n{self.COLORS['JAUNE']}🎤 NOTES VOCALES:{self.COLORS['RESET']}")
        print(f"  Total: {total_notes}")
        
        # Dernières activités
        print(f"\n{self.COLORS['JAUNE']}🕒 DERNIÈRES ACTIVITÉS:{self.COLORS['RESET']}")
        self.cursor.execute("""
            SELECT * FROM (
                SELECT date, 'email' as type, sujet as detail FROM emails 
                UNION ALL
                SELECT date || ' ' || heure as date, 'rdv' as type, titre as detail FROM rendezvous
                UNION ALL
                SELECT date, 'note' as type, nom_fichier as detail FROM notes_vocales
            ) ORDER BY date DESC LIMIT 5
        """)
        
        activites = self.cursor.fetchall()
        for date, type_act, detail in activites:
            icone = "📧" if type_act == "email" else "📅" if type_act == "rdv" else "🎤"
            print(f"  {icone} {date}: {detail[:40]}")
        
        print(f"\n{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_recherche(self):
        """Recherche intelligente"""
        self.clear_screen()
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        print(f"{self.COLORS['VERT']}🔍 RECHERCHE INTELLIGENTE{self.COLORS['RESET']}")
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        
        terme = input("Mot-clé à rechercher: ").strip()
        
        if not terme:
            print(f"{self.COLORS['ROUGE']}❌ Terme de recherche vide{self.COLORS['RESET']}")
            input("\nAppuyez sur Entrée pour continuer...")
            return
        
        print(f"\n{self.COLORS['JAUNE']}Résultats pour '{terme}':{self.COLORS['RESET']}")
        
        # Recherche dans les emails
        self.cursor.execute("""
            SELECT id, sujet, expediteur, date 
            FROM emails 
            WHERE sujet LIKE ? OR expediteur LIKE ? OR contenu LIKE ?
            LIMIT 5
        """, (f'%{terme}%', f'%{terme}%', f'%{terme}%'))
        
        emails = self.cursor.fetchall()
        if emails:
            print(f"\n{self.COLORS['BLEU']}📧 EMAILS ({len(emails)}):{self.COLORS['RESET']}")
            for id_email, sujet, expediteur, date in emails:
                print(f"  [{id_email}] {sujet[:40]}... - {expediteur} ({date})")
        
        # Recherche dans les rendez-vous
        self.cursor.execute("""
            SELECT id, titre, date, heure, lieu 
            FROM rendezvous 
            WHERE titre LIKE ? OR description LIKE ? OR lieu LIKE ? OR participants LIKE ?
            LIMIT 5
        """, (f'%{terme}%', f'%{terme}%', f'%{terme}%', f'%{terme}%'))
        
        rdvs = self.cursor.fetchall()
        if rdvs:
            print(f"\n{self.COLORS['BLEU']}📅 RENDEZ-VOUS ({len(rdvs)}):{self.COLORS['RESET']}")
            for id_rdv, titre, date, heure, lieu in rdvs:
                print(f"  [{id_rdv}] {titre[:40]}... - {date} {heure} à {lieu}")
        
        if not emails and not rdvs:
            print(f"{self.COLORS['JAUNE']}⚠️  Aucun résultat trouvé{self.COLORS['RESET']}")
        
        print(f"\n{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_notes_vocales(self):
        """Menu de gestion des notes vocales"""
        # Pour Alpine, on peut simuler la transcription
        # ou utiliser des outils légers comme Vosk (hors scope ici)
        
        self.clear_screen()
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        print(f"{self.COLORS['VERT']}🎤 NOTES VOCALES (SIMULATION){self.COLORS['RESET']}")
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        
        print("\n⚠️  Sur Alpine Linux, la transcription audio nécessite")
        print("l'installation de paquets supplémentaires.")
        print("\nOptions disponibles:")
        print("1. Simuler une note vocale")
        print("2. Lister les notes existantes")
        print("3. Retour")
        
        choix = input("\nChoix: ").strip()
        
        if choix == "1":
            self.simuler_note_vocale()
        elif choix == "2":
            self.lister_notes_vocales()
    
    def simuler_note_vocale(self):
        """Simuler l'ajout d'une note vocale"""
        print(f"\n{self.COLORS['VERT']}🎤 SIMULATION NOTE VOCALE:{self.COLORS['RESET']}")
        nom = input("Nom de la note: ")
        transcription = input("Transcription (texte): ")
        
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        self.cursor.execute(
            "INSERT INTO notes_vocales (nom_fichier, transcription, date) VALUES (?, ?, ?)",
            (nom, transcription, date)
        )
        self.conn.commit()
        print(f"{self.COLORS['VERT']}✅ Note vocale enregistrée!{self.COLORS['RESET']}")
        input("\nAppuyez sur Entrée pour continuer...")
    
    def lister_notes_vocales(self):
        """Lister les notes vocales"""
        self.cursor.execute("SELECT id, nom_fichier, date FROM notes_vocales ORDER BY date DESC")
        notes = self.cursor.fetchall()
        
        if notes:
            print(f"\n{self.COLORS['JAUNE']}📋 NOTES VOCALES:{self.COLORS['RESET']}")
            for id_note, nom, date in notes:
                print(f"  {id_note:3d} | {nom:30} | {date}")
        else:
            print(f"{self.COLORS['JAUNE']}⚠️  Aucune note vocale{self.COLORS['RESET']}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    def menu_parametres(self):
        """Menu des paramètres"""
        while True:
            self.clear_screen()
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            print(f"{self.COLORS['VERT']}⚙️  PARAMÈTRES{self.COLORS['RESET']}")
            print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
            
            print(f"\n{self.COLORS['JAUNE']}1. Vérifier l'environnement{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}2. Exporter les données{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}3. Réinitialiser la base{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}4. Informations système{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}5. Mettre à jour l'agent{self.COLORS['RESET']}")
            print(f"{self.COLORS['JAUNE']}6. Retour{self.COLORS['RESET']}")
            
            choix = input(f"\n{self.COLORS['VERT']}Paramètre: {self.COLORS['RESET']}").strip()
            
            if choix == "1":
                self.verifier_environnement()
            elif choix == "2":
                self.exporter_donnees()
            elif choix == "3":
                self.reinitialiser_base()
            elif choix == "4":
                self.informations_systeme()
            elif choix == "5":
                self.mettre_a_jour()
            elif choix == "6":
                break
            else:
                print(f"{self.COLORS['ROUGE']}❌ Choix invalide{self.COLORS['RESET']}")
            
            input("\nAppuyez sur Entrée pour continuer...")
    
    def verifier_environnement(self):
        """Vérifier l'environnement Alpine"""
        print(f"\n{self.COLORS['JAUNE']}🔍 VÉRIFICATION ENVIRONNEMENT:{self.COLORS['RESET']}")
        
        # Vérifier Python
        try:
            version_python = sys.version.split()[0]
            print(f"✅ Python: {version_python}")
        except:
            print(f"❌ Python: Non détecté")
        
        # Vérifier SQLite
        try:
            version_sqlite = sqlite3.version
            print(f"✅ SQLite: {version_sqlite}")
        except:
            print(f"❌ SQLite: Non détecté")
        
        # Vérifier espace disque
        try:
            stat = os.statvfs('/')
            espace_total = stat.f_blocks * stat.f_frsize / (1024**3)  # Go
            espace_libre = stat.f_bfree * stat.f_frsize / (1024**3)   # Go
            print(f"💾 Espace disque: {espace_libre:.1f} Go libre / {espace_total:.1f} Go total")
        except:
            print("💾 Espace disque: Non vérifiable")
    
    def exporter_donnees(self):
        """Exporter les données en JSON"""
        try:
            data = {
                "emails": [],
                "rendezvous": [],
                "notes_vocales": []
            }
            
            # Exporter emails
            self.cursor.execute("SELECT * FROM emails")
            for row in self.cursor.fetchall():
                data["emails"].append({
                    "id": row[0],
                    "sujet": row[1],
                    "expediteur": row[2],
                    "date": row[4]
                })
            
            # Exporter rendez-vous
            self.cursor.execute("SELECT * FROM rendezvous")
            for row in self.cursor.fetchall():
                data["rendezvous"].append({
                    "id": row[0],
                    "titre": row[1],
                    "date": row[3],
                    "heure": row[4]
                })
            
            # Sauvegarder
            with open("export_donnees.json", "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"{self.COLORS['VERT']}✅ Données exportées dans export_donnees.json{self.COLORS['RESET']}")
            
        except Exception as e:
            print(f"{self.COLORS['ROUGE']}❌ Erreur export: {e}{self.COLORS['RESET']}")
    
    def reinitialiser_base(self):
        """Réinitialiser la base de données"""
        confirm = input(f"{self.COLORS['ROUGE']}⚠️  Effacer TOUTES les données? (oui/non): {self.COLORS['RESET']}")
        if confirm.lower() == "oui":
            try:
                self.conn.close()
                os.remove(self.db_file)
                self.init_database()
                print(f"{self.COLORS['VERT']}✅ Base réinitialisée!{self.COLORS['RESET']}")
            except Exception as e:
                print(f"{self.COLORS['ROUGE']}❌ Erreur: {e}{self.COLORS['RESET']}")
    
    def informations_systeme(self):
        """Afficher les informations système"""
        print(f"\n{self.COLORS['JAUNE']}💻 INFORMATIONS SYSTÈME:{self.COLORS['RESET']}")
        print(f"Système: {sys.platform}")
        print(f"Version Python: {sys.version}")
        print(f"Répertoire courant: {os.getcwd()}")
        print(f"Utilisateur: {os.getenv('USER', 'inconnu')}")
        print(f"Date/heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def mettre_a_jour(self):
        """Mettre à jour l'agent (simulation)"""
        print(f"\n{self.COLORS['JAUNE']}🔄 MISE À JOUR:{self.COLORS['RESET']}")
        print("Cette fonctionnalité téléchargerait la dernière version")
        print("depuis un dépôt Git si configuré.")
        print("\nPour l'instant, c'est une simulation.")
        print(f"\nVersion actuelle: {self.version}")
        print("Dernière version disponible: 2.1.0")
        
        choix = input(f"\n{self.COLORS['VERT']}Simuler la mise à jour? (oui/non): {self.COLORS['RESET']}")
        if choix.lower() == "oui":
            self.version = "2.1.0"
            print(f"{self.COLORS['VERT']}✅ Version mise à jour à {self.version}{self.COLORS['RESET']}")
    
    def afficher_aide(self):
        """Afficher l'aide"""
        self.clear_screen()
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        print(f"{self.COLORS['VERT']}ℹ️  AIDE - AGENT IA GRATUIT{self.COLORS['RESET']}")
        print(f"{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        
        print(f"\n{self.COLORS['JAUNE']}DESCRIPTION:{self.COLORS['RESET']}")
        print("Cet agent IA gratuit vous aide à gérer:")
        print("  • Vos emails (organisation, recherche)")
        print("  • Vos rendez-vous (planification, rappels)")
        print("  • Vos notes vocales (transcription, gestion)")
        
        print(f"\n{self.COLORS['JAUNE']}COMMANDES RAPIDES:{self.COLORS['RESET']}")
        print("  Dans le menu principal: chiffres 0-7")
        print("  Dans les sous-menus: commandes textuelles")
        
        print(f"\n{self.COLORS['JAUNE']}ASTUCES:{self.COLORS['RESET']}")
        print("  • Utilisez 'rechercher' pour trouver rapidement")
        print("  • Exportez régulièrement vos données")
        print("  • Consultez les statistiques pour suivre votre activité")
        
        print(f"\n{self.COLORS['JAUNE']}POUR ALLER PLUS LOIN:{self.COLORS['RESET']}")
        print("Pour une reconnaissance vocale réelle sur Alpine:")
        print("  apk add sox pulseaudio vosk-model-fr-0.22")
        print("  pip install vosk sounddevice")
        
        print(f"\n{self.COLORS['CYAN']}{'='*50}{self.COLORS['RESET']}")
        input("\nAppuyez sur Entrée pour continuer...")
    
    def clear_screen(self):
        """Effacer l'écran du terminal"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def enregistrer_statistique(self, action, details=""):
        """Enregistrer une action dans les statistiques"""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            "INSERT INTO statistiques (date, action, details) VALUES (?, ?, ?)",
            (date, action, details)
        )
        self.conn.commit()

# Fonctions supplémentaires pour la ligne de commande
def main():
    """Point d'entrée principal"""
    try:
        agent = AgentIAGratuit()
        
        # Gestion des arguments de ligne de commande
        if len(sys.argv) > 1:
            if sys.argv[1] == "--version":
                print(f"Agent IA Gratuit v{agent.version}")
                return
            elif sys.argv[1] == "--stats":
                agent.menu_statistiques()
                return
            elif sys.argv[1] == "--help":
                agent.afficher_aide()
                return
        
        # Mode interactif par défaut
        agent.afficher_menu()
        
    except KeyboardInterrupt:
        print(f"\n{agent.COLORS['JAUNE']}👋 Interruption - Au revoir!{agent.COLORS['RESET']}")
    except Exception as e:
        print(f"{agent.COLORS['ROUGE']}❌ Erreur fatale: {e}{agent.COLORS['RESET']}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
