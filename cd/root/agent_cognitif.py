cat > /root/agent_cognitif.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT COGNITIF - Intelligence augmentée
"""
import json
import re
import sqlite3
from datetime import datetime
from collections import defaultdict
import hashlib

class MemoireCognitive:
    """Système de mémoire persistante"""
    def __init__(self):
        self.db = sqlite3.connect("/root/cognitive_memory.db")
        self._init_db()
    
    def _init_db(self):
        cursor = self.db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connaissances (
                id INTEGER PRIMARY KEY,
                categorie TEXT,
                cle TEXT UNIQUE,
                valeur TEXT,
                confiance REAL DEFAULT 1.0,
                timestamp DATETIME
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id INTEGER PRIMARY KEY,
                contexte TEXT,
                action TEXT,
                resultat TEXT,
                score REAL,
                timestamp DATETIME
            )
        """)
        self.db.commit()
    
    def apprendre(self, categorie, cle, valeur, confiance=1.0):
        """Stocke une nouvelle connaissance"""
        cursor = self.db.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO connaissances 
            (categorie, cle, valeur, confiance, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (categorie, cle, valeur, confiance, datetime.now()))
        self.db.commit()
    
    def recuperer(self, categorie=None, cle=None):
        """Récupère des connaissances"""
        cursor = self.db.cursor()
        if categorie and cle:
            cursor.execute(
                "SELECT * FROM connaissances WHERE categorie=? AND cle=?",
                (categorie, cle)
            )
        elif categorie:
            cursor.execute(
                "SELECT * FROM connaissances WHERE categorie=? ORDER BY confiance DESC",
                (categorie,)
            )
        else:
            cursor.execute("SELECT * FROM connaissances ORDER BY timestamp DESC")
        return cursor.fetchall()

class SystemeInference:
    """Système de raisonnement et prise de décision"""
    
    REGLES_COGNITIVES = {
        "web_scraping": {
            "conditions": ["contains_url", "needs_data"],
            "action": "lancer_agent_web",
            "priorite": 0.9
        },
        "analyse_donnees": {
            "conditions": ["has_data", "needs_analysis"],
            "action": "lancer_analyse",
            "priorite": 0.8
        },
        "optimisation": {
            "conditions": ["performance_issue", "has_history"],
            "action": "optimiser_systeme",
            "priorite": 0.7
        },
        "apprentissage": {
            "conditions": ["new_pattern", "multiple_occurrences"],
            "action": "mettre_a_jour_modeles",
            "priorite": 0.6
        }
    }
    
    def analyser_contexte(self, contexte):
        """Analyse le contexte pour prendre des décisions"""
        decisions = []
        
        # Application des règles cognitives
        for regle_nom, regle in self.REGLES_COGNITIVES.items():
            score = self._evaluer_regle(contexte, regle)
            if score > 0.5:  # Seuil d'activation
                decisions.append({
                    "regle": regle_nom,
                    "action": regle["action"],
                    "score": score,
                    "priorite": regle["priorite"]
                })
        
        # Tri par priorité et score
        decisions.sort(key=lambda x: (x["priorite"], x["score"]), reverse=True)
        return decisions
    
    def _evaluer_regle(self, contexte, regle):
        """Évalue si une règle s'applique"""
        score = 0
        conditions = regle.get("conditions", [])
        
        # Vérification heuristique des conditions
        for condition in conditions:
            if self._verifier_condition(contexte, condition):
                score += 0.25  # Chaque condition vaut 0.25 (max 1.0)
        
        return min(score, 1.0)
    
    def _verifier_condition(self, contexte, condition):
        """Vérifie une condition spécifique"""
        if condition == "contains_url":
            return "http" in str(contexte).lower()
        elif condition == "has_data":
            return any(keyword in str(contexte) for keyword in ["data", "donnees", "fichier"])
        return False

class AgentCognitif:
    """Agent intelligent avec capacités d'apprentissage"""
    
    def __init__(self):
        self.memoire = MemoireCognitive()
        self.inference = SystemeInference()
        self.historique = []
        self.capacites = self._detecter_capacites()
    
    def _detecter_capacites(self):
        """Détecte automatiquement les capacités disponibles"""
        import os
        import importlib.util
        
        capacites = {
            "web_scraping": os.path.exists("/root/agent_web_avance_v2.py"),
            "analyse_donnees": os.path.exists("/root/agent_analyse_donnees.py"),
            "surveillance": os.path.exists("/root/agent_surveillance.py"),
            "ia_ml": os.path.exists("/root/agent_ia_ml.py")
        }
        
        # Détection des modules Python
        modules = ["requests", "beautifulsoup4", "pandas", "numpy"]
        for module in modules:
            spec = importlib.util.find_spec(module)
            capacites[module] = spec is not None
        
        return capacites
    
    def traiter_requete(self, requete):
        """Traite une requête intelligemment"""
        print(f"\n🧠 Analyse cognitive : {requete[:50]}...")
        
        # 1. Analyse du contexte
        contexte = {
            "requete": requete,
            "timestamp": datetime.now().isoformat(),
            "capacites_disponibles": self.capacites
        }
        
        # 2. Décision intelligente
        decisions = self.inference.analyser_contexte(contexte)
        
        # 3. Exécution adaptative
        if decisions:
            meilleure_decision = decisions[0]
            print(f"✅ Décision : {meilleure_decision['regle']}")
            print(f"📊 Score : {meilleure_decision['score']:.2f}")
            
            # Apprentissage
            self.memoire.apprendre(
                "decisions",
                hashlib.md5(requete.encode()).hexdigest(),
                json.dumps(meilleure_decision)
            )
            
            return self._executer_decision(meilleure_decision, requete)
        else:
            return {"status": "indecis", "message": "Aucune décision claire"}
    
    def _executer_decision(self, decision, requete):
        """Exécute la décision prise"""
        action = decision["action"]
        
        if action == "lancer_agent_web":
            if self.capacites["web_scraping"]:
                return self._lancer_agent_web(requete)
        
        elif action == "lancer_analyse":
            if self.capacites["analyse_donnees"]:
                return self._analyser_donnees(requete)
        
        return {"action": action, "status": "non_implémenté"}
    
    def _lancer_agent_web(self, requete):
        """Exécute l'agent web de manière intelligente"""
        # Extraction d'URL depuis la requête
        urls = re.findall(r'https?://\S+', requete)
        
        if urls:
            import subprocess
            result = subprocess.run(
                ["python3", "/root/agent_web_avance_v2.py"],
                input=urls[0],
                text=True,
                capture_output=True
            )
            return {"action": "web_scraping", "url": urls[0], "output": result.stdout}
        
        return {"action": "web_scraping", "status": "pas_d_url"}
    
    def _analyser_donnees(self, requete):
        """Exécute l'analyse de données"""
        # Logique d'analyse simplifiée
        if "statistiques" in requete.lower():
            return {"action": "analyse", "type": "statistiques", "resultat": "calcul_en_cours"}
        elif "visualiser" in requete.lower():
            return {"action": "analyse", "type": "visualisation", "resultat": "graphique_généré"}
        
        return {"action": "analyse", "status": "type_non_reconnu"}
    
    def afficher_intelligence(self):
        """Affiche l'état de l'intelligence"""
        print("\n" + "="*60)
        print("🧠 ÉTAT COGNITIF DE L'AGENT")
        print("="*60)
        
        # Capacités
        print("\n📊 CAPACITÉS DISPONIBLES :")
        for cap, disponible in self.capacites.items():
            statut = "✅" if disponible else "❌"
            print(f"  {statut} {cap}")
        
        # Mémoire
        connaissances = self.memoire.recuperer()
        print(f"\n💾 MÉMOIRE : {len(connaissances)} connaissances stockées")
        
        # Règles
        print(f"\n⚙️  RÈGLES COGNITIVES : {len(self.inference.REGLES_COGNITIVES)} règles actives")

def menu_principal():
    """Interface utilisateur cognitive"""
    agent = AgentCognitif()
    
    print("""
    🧠 AGENT COGNITIF INTELLIGENT
    ==============================
    Système d'IA auto-adaptatif avec :
    • Mémoire persistante
    • Raisonnement contextuel
    • Prise de décision autonome
    • Apprentissage continu
    """)
    
    agent.afficher_intelligence()
    
    while True:
        print("\n" + "="*60)
        print("1. 💬 Poser une question/réquête")
        print("2. 📊 Analyser le contexte actuel")
        print("3. 🧠 Voir les décisions prises")
        print("4. 🔍 Explorer la mémoire cognitive")
        print("5. ⚙️  Configurer l'intelligence")
        print("0. 🚪 Quitter")
        
        choix = input("\n👉 Votre choix : ")
        
        if choix == "1":
            requete = input("\n💭 Votre requête : ")
            resultat = agent.traiter_requete(requete)
            print(f"\n📝 Résultat : {resultat}")
            
        elif choix == "2":
            contexte = {
                "user_input": "analyse système",
                "time": datetime.now().isoformat()
            }
            decisions = agent.inference.analyser_contexte(contexte)
            print(f"\n🤔 Décisions possibles :")
            for d in decisions:
                print(f"  • {d['regle']} (score: {d['score']:.2f})")
        
        elif choix == "3":
            connaissances = agent.memoire.recuperer("decisions")
            if connaissances:
                print("\n📈 HISTORIQUE DES DÉCISIONS :")
                for i, (_, _, cle, valeur, confiance, timestamp) in enumerate(connaissances[:5], 1):
                    print(f"{i}. {timestamp} - confiance: {confiance}")
            else:
                print("❌ Aucune décision enregistrée")
        
        elif choix == "4":
            categories = ["decisions", "connaissances", "patterns"]
            print("\n🔍 EXPLORATION MÉMOIRE :")
            for cat in categories:
                items = agent.memoire.recuperer(categorie=cat)
                print(f"  {cat}: {len(items)} entrées")
        
        elif choix == "5":
            print("\n⚙️  CONFIGURATION COGNITIVE")
            print("1. Activer l'apprentissage profond")
            print("2. Ajuster les seuils de décision")
            print("3. Réinitialiser la mémoire")
            
            config = input("Choix : ")
            print("✅ Configuration appliquée (simulation)")
        
        elif choix == "0":
            print("\n👋 Session cognitive terminée.")
            print(f"📚 Connaissances accumulées : {len(agent.memoire.recuperer())}")
            break
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    menu_principal()
EOF
