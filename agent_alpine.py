#!/usr/bin/env python3
# agent_alpine.py - Version optimisée pour Alpine

import os
import sys
import sqlite3
from datetime import datetime

class AlpineAgent:
    """Agent IA léger pour Alpine Linux"""
    
    def __init__(self):
        self.db_path = "/root/Agent-ia-gratuit/agent.db"
        self.init_database()
        
    def init_database(self):
        """Initialiser la base de données SQLite"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Table emails
        c.execute('''CREATE TABLE IF NOT EXISTS emails
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     sujet TEXT,
                     expediteur TEXT,
                     date TEXT,
                     traite INTEGER DEFAULT 0)''')
        
        # Table rendez-vous
        c.execute('''CREATE TABLE IF NOT EXISTS rendezvous
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     date TEXT,
                     heure TEXT,
                     participant TEXT,
                     lieu TEXT,
                     objet TEXT)''')
        
        # Table notes
        c.execute('''CREATE TABLE IF NOT EXISTS notes
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     contenu TEXT,
                     date TEXT)''')
        
        conn.commit()
        conn.close()
        print("✅ Base de données initialisée")
    
    def afficher_menu(self):
        """Afficher le menu principal"""
        while True:
            print("\n" + "="*40)
            print("🤖 AGENT IA - Alpine Linux Edition")
            print("="*40)
            print("1. 📧 Gérer les emails")
            print("2. 📅 Gérer les rendez-vous")
            print("3. 🎤 Gérer les notes vocales")
            print("4. 📊 Statistiques")
            print("5. ⚙️  Configuration")
            print("6. ❌ Quitter")
            print("="*40)
            
            choix = input("Votre choix (1-6): ").strip()
            
            if choix == "1":
                self.gerer_emails()
            elif choix == "2":
                self.gerer_rendezvous()
            elif choix == "3":
                self.gerer_notes()
            elif choix == "4":
                self.afficher_stats()
            elif choix == "5":
                self.configuration()
            elif choix == "6":
                print("👋 Au revoir!")
                sys.exit(0)
    
    def gerer_emails(self):
        """Gestion des emails"""
        print("\n📧 GESTION DES EMAILS")
        print("-" * 30)
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM emails")
        total = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM emails WHERE traite=1")
        traites = c.fetchone()[0]
        
        print(f"Emails: {total} (dont {traites} traités)")
        print("\nOptions:")
        print("1. Ajouter un email")
        print("2. Lister les emails")
        print("3. Marquer comme traité")
        print("4. Retour")
        
        choix = input("Choix: ")
        
        if choix == "1":
            sujet = input("Sujet: ")
            expediteur = input("Expéditeur: ")
            date = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            c.execute("INSERT INTO emails (sujet, expediteur, date) VALUES (?, ?, ?)",
                     (sujet, expediteur, date))
            conn.commit()
            print("✅ Email ajouté!")
        
        conn.close()
    
    def afficher_stats(self):
        """Afficher les statistiques"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM emails")
        emails = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM rendezvous")
        rdv = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM notes")
        notes = c.fetchone()[0]
        
        print("\n📊 STATISTIQUES")
        print("=" * 30)
        print(f"📧 Emails: {emails}")
        print(f"📅 Rendez-vous: {rdv}")
        print(f"🎤 Notes vocales: {notes}")
        print("=" * 30)
        
        conn.close()
    
    def configuration(self):
        """Menu de configuration"""
        print("\n⚙️  CONFIGURATION")
        print("-" * 20)
        print("1. Réinitialiser la base")
        print("2. Vérifier les dépendances")
        print("3. Mettre à jour l'agent")
        print("4. Retour")
        
        choix = input("Choix: ")
        
        if choix == "1":
            confirm = input("⚠️  Effacer toutes les données? (oui/non): ")
            if confirm.lower() == "oui":
                os.remove(self.db_path)
                self.init_database()
                print("✅ Base réinitialisée!")
        elif choix == "2":
            self.verifier_dependances()

    def verifier_dependances(self):
        """Vérifier les dépendances installées"""
        print("\n🔍 VÉRIFICATION DES DÉPENDANCES")
        
        deps = [
            ("python3", "Python 3"),
            ("pip3", "Pip"),
            ("sqlite3", "SQLite3")
        ]
        
        for cmd, nom in deps:
            if os.system(f"which {cmd} > /dev/null 2>&1") == 0:
                print(f"✅ {nom} - Installé")
            else:
                print(f"❌ {nom} - Manquant")

def main():
    """Point d'entrée principal"""
    print("🚀 Agent IA - Démarrage...")
    
    agent = AlpineAgent()
    agent.afficher_menu()

if __name__ == "__main__":
    main()
