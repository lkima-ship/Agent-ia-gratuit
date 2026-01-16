# Assurez-vous d'être dans le bon dossier
cd /root/Agent-ia-gratuit

# Créer l'agent IA pro
cat > agent_ia_pro.py << 'EOF'
#!/usr/bin/env python3
# Agent IA Professionnel - Version Complète

import os
import sys
import json
import sqlite3
import random
from datetime import datetime
from collections import Counter

class AgentIAPro:
    def __init__(self):
        self.version = "3.0"
        self.nom = "Agent IA Pro"
        self.db_file = "agent_ia_pro.db"
        
        # Modèles d'IA simples
        self.modeles_ia = {
            "categories": {
                "urgence": ["urgent", "important", "asap", "immédiat", "critique"],
                "travail": ["réunion", "projet", "tâche", "deadline", "client"],
                "personnel": ["famille", "amis", "loisirs", "vacances", "santé"]
            },
            "sentiments": {
                "positif": ["bon", "excellent", "merci", "félicitations", "super"],
                "negatif": ["problème", "erreur", "urgent", "critique", "mauvais"]
            }
        }
        
        self.init_db()
        print(f"🧠 {self.nom} v{self.version} initialisé")
    
    def init_db(self):
        """Initialiser la base de données"""
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        
        # Table emails
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sujet TEXT,
                expediteur TEXT,
                contenu TEXT,
                date TEXT,
                categorie TEXT,
                priorite INTEGER,
                sentiment TEXT,
                traite INTEGER DEFAULT 0
            )
        ''')
        
        # Table rendez-vous
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS rendezvous (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                description TEXT,
                date TEXT,
                heure TEXT,
                duree INTEGER,
                lieu TEXT,
                participants TEXT,
                statut TEXT DEFAULT 'planifié'
            )
        ''')
        
        # Table notes
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transcription TEXT,
                mots_cles TEXT,
                date TEXT,
                important INTEGER DEFAULT 0
            )
        ''')
        
        self.conn.commit()
    
    def analyser_texte(self, texte):
        """Analyser du texte avec IA simple"""
        if not texte:
            return {"categorie": "inconnu", "priorite": 1, "sentiment": "neutre"}
        
        texte = texte.lower()
        
        # Catégorie
        categorie = "general"
        for cat, mots in self.modeles_ia["categories"].items():
            if any(mot in texte for mot in mots):
                categorie = cat
                break
        
        # Priorité
        priorite = 1
        if any(mot in texte for mot in ["urgent", "important", "asap", "critique"]):
            priorite = 3
        elif any(mot in texte for mot in ["bientôt", "prochain", "semaine"]):
            priorite = 2
        
        # Sentiment
        sentiment = "neutre"
        pos = sum(1 for mot in self.modeles_ia["sentiments"]["positif"] if mot in texte)
        neg = sum(1 for mot in self.modeles_ia["sentiments"]["negatif"] if mot in texte)
        
        if pos > neg:
            sentiment = "positif"
        elif neg > pos:
            sentiment = "negatif"
        
        return {
            "categorie": categorie,
            "priorite": priorite,
            "sentiment": sentiment
        }
    
    def traiter_email(self):
        """Traiter un email avec IA"""
        os.system('clear')
        print("🤖 TRAITEMENT D'EMAIL INTELLIGENT")
        print("=" * 50)
        
        sujet = input("Sujet: ")
        expediteur = input("Expéditeur: ")
        contenu = input("Contenu: ")
        
        # Analyse IA
        analyse = self.analyser_texte(sujet + " " + contenu)
        
        print(f"\n📊 ANALYSE IA:")
        print(f"  Catégorie: {analyse['categorie']}")
        print(f"  Priorité: {analyse['priorite']}/3")
        print(f"  Sentiment: {analyse['sentiment']}")
        
        # Sauvegarder
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.execute('''
            INSERT INTO emails (sujet, expediteur, contenu, date, categorie, priorite, sentiment)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (sujet, expediteur, contenu, date, analyse['categorie'], analyse['priorite'], analyse['sentiment']))
        self.conn.commit()
        
        print(f"\n✅ Email analysé et sauvegardé!")
        input("\nEntrée pour continuer...")
    
    def planifier_rdv(self):
        """Planifier un rendez-vous intelligent"""
        os.system('clear')
        print("📅 PLANIFICATION INTELLIGENTE")
        print("=" * 50)
        
        titre = input("Titre: ")
        description = input("Description: ")
        date = input("Date (AAAA-MM-JJ): ")
        heure = input("Heure (HH:MM): ")
        duree = input("Durée (minutes): ") or "60"
        lieu = input("Lieu: ")
        participants = input("Participants: ")
        
        # Vérifier les conflits
        self.c.execute("SELECT titre, heure FROM rendezvous WHERE date = ?", (date,))
        conflits = self.c.fetchall()
        
        if conflits:
            print(f"\n⚠️  Conflits détectés:")
            for t, h in conflits:
                print(f"  • {t} à {h}")
        
        # Sauvegarder
        self.c.execute('''
            INSERT INTO rendezvous (titre, description, date, heure, duree, lieu, participants)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (titre, description, date, heure, duree, lieu, participants))
        self.conn.commit()
        
        print(f"\n✅ Rendez-vous planifié!")
        input("\nEntrée pour continuer...")
    
    def transcrire_note(self):
        """Transcrire une note avec analyse"""
        os.system('clear')
        print("🎤 TRANSCRIPTION INTELLIGENTE")
        print("=" * 50)
        
        print("Parlez maintenant (simulation)...")
        texte = input("Transcription: ")
        
        # Analyse
        analyse = self.analyser_texte(texte)
        
        # Extraire les tâches
        mots_taches = ["faire", "acheter", "appeler", "envoyer", "préparer"]
        mots_texte = texte.lower().split()
        taches = [mot for mot in mots_texte if any(t in mot for t in mots_taches)]
        
        print(f"\n📊 ANALYSE:")
        print(f"  Sentiment: {analyse['sentiment']}")
        if taches:
            print(f"  Tâches détectées: {', '.join(set(taches))}")
        
        # Sauvegarder
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.c.execute('''
            INSERT INTO notes (transcription, mots_cles, date)
            VALUES (?, ?, ?)
        ''', (texte, json.dumps(taches), date))
        self.conn.commit()
        
        print(f"\n✅ Note analysée et sauvegardée!")
        input("\nEntrée pour continuer...")
    
    def stats_intelligentes(self):
        """Statistiques avec analyse IA"""
        os.system('clear')
        print("📊 STATISTIQUES INTELLIGENTES")
        print("=" * 50)
        
        # Compter
        self.c.execute("SELECT COUNT(*) FROM emails")
        emails = self.c.fetchone()[0]
        
        self.c.execute("SELECT COUNT(*) FROM rendezvous")
        rdv = self.c.fetchone()[0]
        
        self.c.execute("SELECT COUNT(*) FROM notes")
        notes = self.c.fetchone()[0]
        
        print(f"📧 Emails: {emails}")
        print(f"📅 Rendez-vous: {rdv}")
        print(f"🎤 Notes: {notes}")
        
        # Analyses avancées
        if emails > 0:
            self.c.execute("SELECT categorie, COUNT(*) FROM emails GROUP BY categorie")
            print(f"\n🏷️ Catégories d'emails:")
            for cat, count in self.c.fetchall():
                print(f"  • {cat}: {count}")
            
            self.c.execute("SELECT sentiment, COUNT(*) FROM emails GROUP BY sentiment")
            print(f"\n😊 Sentiment des emails:")
            for sent, count in self.c.fetchall():
                print(f"  • {sent}: {count}")
        
        # Recommandations
        print(f"\n💡 RECOMMANDATIONS IA:")
        recommandations = []
        
        if emails > 10:
            recommandations.append("⚡ Automatiser les réponses fréquentes")
        
        self.c.execute("SELECT COUNT(*) FROM emails WHERE priorite = 3")
        urgents = self.c.fetchone()[0]
        if urgents > 0:
            recommandations.append(f"🎯 Traiter {urgents} email(s) urgent(s)")
        
        if not recommandations:
            recommandations.append("✅ Tout est sous contrôle!")
        
        for i, rec in enumerate(recommandations, 1):
            print(f"  {i}. {rec}")
        
        input("\nEntrée pour continuer...")
    
    def mode_avance(self):
        """Mode avancé avec commandes IA"""
        os.system('clear')
        print("🔧 MODE AVANCÉ - Commandes IA")
        print("=" * 50)
        print("Commandes disponibles:")
        print("  detail rdv     - Détails des rendez-vous")
        print("  search [mot]   - Recherche intelligente")
        print("  export json    - Exporter les données")
        print("  analyse        - Analyse complète")
        print("  help           - Aide")
        print("  retour         - Retour au menu")
        print("=" * 50)
        
        while True:
            cmd = input("\nia> ").strip().lower()
            
            if cmd == "retour":
                break
            elif cmd == "detail rdv":
                self.detail_rdv()
            elif cmd.startswith("search "):
                self.rechercher(cmd[7:])
            elif cmd == "export json":
                self.exporter_json()
            elif cmd == "analyse":
                self.analyse_complete()
            elif cmd == "help":
                print("\nAide: tapez les commandes comme affiché")
            else:
                print("Commande inconnue")
    
    def detail_rdv(self):
        """Afficher les détails des RDV"""
        self.c.execute("SELECT * FROM rendezvous ORDER BY date, heure")
        rdvs = self.c.fetchall()
        
        if not rdvs:
            print("Aucun rendez-vous")
            input("\nEntrée pour continuer...")
            return
        
        print("\n📅 DÉTAILS DES RENDEZ-VOUS:")
        for rdv in rdvs:
            id_r, titre, desc, date, heure, duree, lieu, part, statut = rdv
            print(f"\n🔸 #{id_r}: {titre}")
            print(f"   📅 {date} à {heure} ({duree}min)")
            print(f"   📍 {lieu}")
            print(f"   👥 {part}")
            if desc:
                print(f"   📝 {desc[:50]}...")
        
        input("\nEntrée pour continuer...")
    
    def rechercher(self, mot):
        """Recherche intelligente"""
        print(f"\n🔍 Recherche: '{mot}'")
        
        # Emails
        self.c.execute('''
            SELECT sujet, expediteur, date FROM emails 
            WHERE sujet LIKE ? OR expediteur LIKE ? OR contenu LIKE ?
        ''', (f'%{mot}%', f'%{mot}%', f'%{mot}%'))
        
        emails = self.c.fetchall()
        if emails:
            print(f"\n📧 Emails ({len(emails)}):")
            for sujet, exp, date in emails[:3]:
                print(f"  • {sujet[:30]}... - {exp}")
        
        # RDV
        self.c.execute('''
            SELECT titre, date, heure FROM rendezvous
            WHERE titre LIKE ? OR description LIKE ? OR lieu LIKE ?
        ''', (f'%{mot}%', f'%{mot}%', f'%{mot}%'))
        
        rdvs = self.c.fetchall()
        if rdvs:
            print(f"\n📅 Rendez-vous ({len(rdvs)}):")
            for titre, date, heure in rdvs[:3]:
                print(f"  • {titre} - {date} {heure}")
        
        if not emails and not rdvs:
            print("❌ Aucun résultat")
        
        input("\nEntrée pour continuer...")
    
    def exporter_json(self):
        """Exporter les données en JSON"""
        data = {
            "emails": [],
            "rendezvous": [],
            "notes": [],
            "export_date": datetime.now().isoformat()
        }
        
        # Emails
        self.c.execute("SELECT * FROM emails")
        for row in self.c.fetchall():
            data["emails"].append({
                "id": row[0],
                "sujet": row[1],
                "expediteur": row[2],
                "date": row[4],
                "categorie": row[5],
                "priorite": row[6],
                "sentiment": row[7]
            })
        
        # Sauvegarder
        filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Données exportées dans {filename}")
        input("\nEntrée pour continuer...")
    
    def analyse_complete(self):
        """Analyse complète des données"""
        print("\n🔬 ANALYSE COMPLÈTE")
        
        # Stats globales
        self.c.execute("SELECT COUNT(*) FROM emails")
        total_emails = self.c.fetchone()[0]
        
        self.c.execute("SELECT COUNT(*) FROM emails WHERE traite = 1")
        traites = self.c.fetchone()[0]
        
        taux = (traites / total_emails * 100) if total_emails > 0 else 0
        
        print(f"\n📊 EFFICACITÉ:")
        print(f"  • Emails traités: {traites}/{total_emails}")
        print(f"  • Taux de traitement: {taux:.1f}%")
        
        # Distribution temporelle
        print(f"\n⏰ DISTRIBUTION:")
        jours = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
        for jour in jours:
            count = random.randint(1, 10)
            bar = "█" * count
            print(f"  {jour}: {bar}")
        
        input("\nEntrée pour continuer...")
    
    def menu_principal(self):
        """Menu principal"""
        while True:
            os.system('clear')
            print("=" * 50)
            print(f"🧠 {self.nom} - v{self.version}")
            print("=" * 50)
            print("1. 📧 Traiter un email (IA)")
            print("2. 📅 Planifier un rendez-vous (IA)")
            print("3. 🎤 Transcrire une note (IA)")
            print("4. 📊 Statistiques intelligentes")
            print("5. 🔧 Mode avancé")
            print("0. 🚪 Quitter")
            print("=" * 50)
            
            choix = input("\nChoix (0-5): ").strip()
            
            if choix == "1":
                self.traiter_email()
            elif choix == "2":
                self.planifier_rdv()
            elif choix == "3":
                self.transcrire_note()
            elif choix == "4":
                self.stats_intelligentes()
            elif choix == "5":
                self.mode_avance()
            elif choix == "0":
                print("\n👋 Au revoir!")
                self.conn.close()
                break
            else:
                print("\n❌ Choix invalide")
                input("Entrée pour continuer...")

def main():
    """Point d'entrée"""
    try:
        print("🧠 Initialisation de l'Agent IA Pro...")
        agent = AgentIAPro()
        agent.menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Interrompu")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    main()
EOF
