cd /root/Agent-ia-gratuit && cat > agent_ia_pro_final.py << 'EOF'
#!/usr/bin/env python3
"""
Agent IA Gratuit - Version Professionnelle
Pour iSH sur iPhone
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
DB_FILE = "agent_ia.db"
BACKUP_DIR = "backups"
EXPORT_DIR = "exports"

def create_directories():
    """Créer les dossiers nécessaires"""
    for directory in [BACKUP_DIR, EXPORT_DIR]:
        Path(directory).mkdir(exist_ok=True)

class Database:
    """Gestionnaire de base de données"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialiser la base de données"""
        tables = [
            """CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                priority INTEGER DEFAULT 1,
                category TEXT,
                response TEXT,
                processed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                duration INTEGER DEFAULT 60,
                location TEXT,
                participants TEXT,
                notes TEXT,
                confirmed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE IF NOT EXISTS voice_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT,
                transcription TEXT,
                summary TEXT,
                duration INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            
            """CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                priority TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )"""
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        for table in tables:
            cursor.execute(table)
        conn.commit()
        conn.close()
    
    def execute(self, query, params=()):
        """Exécuter une requête"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id
    
    def fetch_all(self, query, params=()):
        """Récupérer tous les résultats"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return results
    
    def get_stats(self):
        """Obtenir les statistiques"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        cursor.execute("SELECT COUNT(*) FROM emails")
        stats['emails'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM appointments")
        stats['appointments'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM voice_notes")
        stats['voice_notes'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tasks")
        stats['tasks'] = cursor.fetchone()[0]
        
        conn.close()
        return stats

class AIService:
    """Service d'intelligence artificielle"""
    
    def __init__(self):
        self.available = False
    
    def analyze_email(self, content):
        """Analyser un email"""
        # Simulation d'IA
        keywords = ["urgent", "important", "réunion", "projet", "deadline"]
        found_keywords = [kw for kw in keywords if kw in content.lower()]
        
        priority = 1
        if "urgent" in content.lower():
            priority = 5
        elif "important" in content.lower():
            priority = 3
        
        category = "work" if any(kw in content.lower() for kw in ["réunion", "projet", "deadline"]) else "personal"
        
        return {
            "priority": priority,
            "category": category,
            "keywords": found_keywords,
            "suggested_response": "Je traite votre demande et reviens vers vous rapidement."
        }
    
    def generate_summary(self, text, max_length=100):
        """Générer un résumé"""
        if len(text) <= max_length:
            return text
        return text[:max_length-3] + "..."

class AgentIAPro:
    """Agent IA Professionnel"""
    
    def __init__(self):
        create_directories()
        self.db = Database(DB_FILE)
        self.ai = AIService()
        self.show_welcome()
    
    def show_welcome(self):
        """Afficher le message de bienvenue"""
        print("╔══════════════════════════════════════╗")
        print("║      🤖 AGENT IA PROFESSIONNEL       ║")
        print("║      Version 3.0 - iSH Edition       ║")
        print("╚══════════════════════════════════════╝")
        print()
        print("📁 Base de données :", DB_FILE)
        print("💾 Backups :", BACKUP_DIR)
        print("📤 Exports :", EXPORT_DIR)
        print()
    
    def process_email(self):
        """Traiter un email"""
        print("\n" + "="*50)
        print("📧 NOUVEL EMAIL")
        print("="*50)
        
        sender = input("Expéditeur : ")
        subject = input("Sujet : ")
        print("Contenu (tapez END sur une ligne vide pour finir) :")
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        
        content = "\n".join(lines)
        
        if not content:
            print("⚠️  Aucun contenu, email vide.")
            return
        
        # Analyse IA
        print("\n🔍 Analyse en cours...")
        analysis = self.ai.analyze_email(content)
        
        print("\n📊 Analyse terminée :")
        print(f"   Priorité : {analysis['priority']}/5")
        print(f"   Catégorie : {analysis['category']}")
        print(f"   Mots-clés : {', '.join(analysis['keywords'])}")
        print(f"   Réponse suggérée : {analysis['suggested_response']}")
        
        # Enregistrement
        email_id = self.db.execute(
            "INSERT INTO emails (sender, subject, content, priority, category, response) VALUES (?, ?, ?, ?, ?, ?)",
            (sender, subject, content, analysis['priority'], analysis['category'], analysis['suggested_response'])
        )
        
        print(f"\n✅ Email #{email_id} enregistré avec succès !")
    
    def schedule_appointment(self):
        """Planifier un rendez-vous"""
        print("\n" + "="*50)
        print("📅 NOUVEAU RENDEZ-VOUS")
        print("="*50)
        
        title = input("Titre : ")
        date = input("Date (YYYY-MM-DD) : ")
        time = input("Heure (HH:MM) : ")
        duration = input("Durée (minutes, défaut 60) : ") or "60"
        location = input("Lieu : ")
        participants = input("Participants (séparés par des virgules) : ")
        notes = input("Notes : ")
        
        # Validation
        if not title or not date or not time:
            print("❌ Titre, date et heure sont obligatoires.")
            return
        
        appointment_id = self.db.execute(
            """INSERT INTO appointments 
               (title, date, time, duration, location, participants, notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (title, date, time, duration, location, participants, notes)
        )
        
        print(f"\n✅ Rendez-vous #{appointment_id} planifié !")
        print(f"   📍 {location}")
        print(f"   🕐 {date} à {time} ({duration} minutes)")
    
    def add_voice_note(self):
        """Ajouter une note vocale"""
        print("\n" + "="*50)
        print("🎙️ NOUVELLE NOTE VOCALE")
        print("="*50)
        
        print("Options de transcription :")
        print("1. Saisir manuellement")
        print("2. Utiliser une transcription simulée")
        
        choice = input("\nChoix (1-2) : ")
        
        if choice == "1":
            transcription = input("Transcription : ")
        elif choice == "2":
            # Transcriptons simulées
            samples = [
                "Réunion importante demain à 10h sur le nouveau projet.",
                "Rappel : envoyer le rapport financier avant vendredi.",
                "Discussion avec le client confirmée pour jeudi après-midi.",
                "Feedback positif sur la dernière présentation.",
                "Planification des vacances d'été avec l'équipe."
            ]
            import random
            transcription = random.choice(samples)
            print(f"\n📝 Transcription simulée : {transcription}")
        else:
            print("❌ Choix invalide.")
            return
        
        # Résumé automatique
        summary = self.ai.generate_summary(transcription)
        
        note_id = self.db.execute(
            "INSERT INTO voice_notes (transcription, summary) VALUES (?, ?)",
            (transcription, summary)
        )
        
        print(f"\n✅ Note vocale #{note_id} enregistrée !")
        print(f"   📋 Résumé : {summary}")
    
    def show_dashboard(self):
        """Afficher le tableau de bord"""
        print("\n" + "="*50)
        print("📊 TABLEAU DE BORD")
        print("="*50)
        
        stats = self.db.get_stats()
        
        print("\n📈 STATISTIQUES :")
        print(f"   📧 Emails : {stats['emails']}")
        print(f"   📅 Rendez-vous : {stats['appointments']}")
        print(f"   🎙️ Notes vocales : {stats['voice_notes']}")
        print(f"   ✅ Tâches : {stats['tasks']}")
        
        # Derniers emails
        if stats['emails'] > 0:
            print("\n📨 DERNIERS EMAILS :")
            emails = self.db.fetch_all("SELECT sender, subject FROM emails ORDER BY id DESC LIMIT 3")
            for i, email in enumerate(emails, 1):
                print(f"   {i}. {email['sender']} : {email['subject'][:30]}...")
        
        # Prochains rendez-vous
        if stats['appointments'] > 0:
            print("\n📅 PROCHAINS RENDEZ-VOUS :")
            appointments = self.db.fetch_all(
                "SELECT title, date, time FROM appointments WHERE confirmed = 0 ORDER BY date, time LIMIT 3"
            )
            for i, appt in enumerate(appointments, 1):
                print(f"   {i}. {appt['title']} - {appt['date']} à {appt['time']}")
    
    def backup_data(self):
        """Sauvegarder les données"""
        print("\n" + "="*50)
        print("💾 SAUVEGARDE")
        print("="*50)
        
        # Collecter toutes les données
        data = {
            "emails": self.db.fetch_all("SELECT * FROM emails"),
            "appointments": self.db.fetch_all("SELECT * FROM appointments"),
            "voice_notes": self.db.fetch_all("SELECT * FROM voice_notes"),
            "tasks": self.db.fetch_all("SELECT * FROM tasks"),
            "backup_date": datetime.now().isoformat()
        }
        
        # Nom du fichier
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{BACKUP_DIR}/backup_{timestamp}.json"
        
        # Sauvegarde
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Sauvegarde créée : {backup_file}")
        print(f"   📦 Taille : {os.path.getsize(backup_file)} octets")
        print(f"   📊 Contenu :")
        print(f"     - {len(data['emails'])} emails")
        print(f"     - {len(data['appointments'])} rendez-vous")
        print(f"     - {len(data['voice_notes'])} notes vocales")
        print(f"     - {len(data['tasks'])} tâches")
    
    def export_data(self):
        """Exporter les données"""
        print("\n" + "="*50)
        print("📤 EXPORT")
        print("="*50)
        
        print("Formats disponibles :")
        print("1. JSON (complet)")
        print("2. CSV (emails)")
        print("3. Texte (statistiques)")
        
        choice = input("\nChoix (1-3) : ")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if choice == "1":
            # Export JSON
            export_file = f"{EXPORT_DIR}/export_{timestamp}.json"
            data = self.db.get_stats()
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"\n✅ Export JSON : {export_file}")
            
        elif choice == "2":
            # Export CSV
            export_file = f"{EXPORT_DIR}/emails_{timestamp}.csv"
            emails = self.db.fetch_all("SELECT sender, subject, created_at FROM emails")
            
            csv_content = "Expéditeur;Sujet;Date\n"
            for email in emails:
                csv_content += f"{email['sender']};{email['subject']};{email['created_at']}\n"
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            
            print(f"\n✅ Export CSV : {export_file}")
            print(f"   Lignes : {len(emails)}")
            
        elif choice == "3":
            # Export texte
            export_file = f"{EXPORT_DIR}/stats_{timestamp}.txt"
            stats = self.db.get_stats()
            
            with open(export_file, 'w', encoding='utf-8') as f:
                f.write(f"Statistiques Agent IA - {datetime.now()}\n")
                f.write("="*40 + "\n\n")
                f.write(f"Emails : {stats['emails']}\n")
                f.write(f"Rendez-vous : {stats['appointments']}\n")
                f.write(f"Notes vocales : {stats['voice_notes']}\n")
                f.write(f"Tâches : {stats['tasks']}\n")
            
            print(f"\n✅ Export texte : {export_file}")
            
        else:
            print("❌ Choix invalide.")
    
    def clear_database(self):
        """Vider la base de données"""
        print("\n" + "="*50)
        print("🧹 NETTOYAGE")
        print("="*50)
        
        print("⚠️  ATTENTION : Cette action supprime TOUTES les données !")
        confirm = input("Confirmer (tapez 'SUPPRIMER') : ")
        
        if confirm == "SUPPRIMER":
            tables = ["emails", "appointments", "voice_notes", "tasks"]
            for table in tables:
                self.db.execute(f"DELETE FROM {table}")
            print("✅ Base de données vidée.")
        else:
            print("❌ Opération annulée.")
    
    def run(self):
        """Exécuter l'agent"""
        menu_items = [
            ("1", "📧 Traiter un email", self.process_email),
            ("2", "📅 Planifier un rendez-vous", self.schedule_appointment),
            ("3", "🎙️ Ajouter une note vocale", self.add_voice_note),
            ("4", "📊 Tableau de bord", self.show_dashboard),
            ("5", "💾 Sauvegarder", self.backup_data),
            ("6", "📤 Exporter", self.export_data),
            ("7", "🧹 Nettoyer la base", self.clear_database),
            ("8", "❌ Quitter", None)
        ]
        
        while True:
            print("\n" + "="*50)
            print("🤖 MENU PRINCIPAL")
            print("="*50)
            
            for num, label, _ in menu_items:
                print(f"  {num}. {label}")
            
            print("="*50)
            
            choice = input("\nVotre choix (1-8) : ").strip()
            
            if choice == "8":
                print("\n👋 Au revoir !")
                break
            
            for num, label, action in menu_items:
                if choice == num and action:
                    action()
                    input("\n↵ Appuyez sur Entrée pour continuer...")
                    break
            else:
                print("❌ Choix invalide.")

def main():
    """Fonction principale"""
    try:
        agent = AgentIAPro()
        agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
EOF
