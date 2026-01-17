cat > suite_agents_ia.py << 'EOF'
#!/usr/bin/env python3
"""
SUITE COMPLÈTE DES AGENTS IA - MENU PRINCIPAL
"""
import os
import sys
import subprocess

class SuiteAgentsIA:
    def __init__(self):
        self.agents = {
            "1": {
                "nom": "🧠 Agent IA avec ML",
                "fichier": "agent_ia_ml.py",
                "desc": "Analyse sémantique et apprentissage"
            },
            "2": {
                "nom": "📊 Agent Analyse Données",
                "fichier": "agent_analyse_donnees.py",
                "desc": "Analyse CSV, JSON et traitement"
            },
            "3": {
                "nom": "🌐 Agent Web Avancé",
                "fichier": "agent_web_avance.py",
                "desc": "Scraping, API et surveillance web"
            },
            "4": {
                "nom": "🔧 Agent Surveillance Système",
                "fichier": "agent_surveillance.py",
                "desc": "Monitoring CPU, mémoire, disque"
            },
            "5": {
                "nom": "🤖 Agent IA Simple",
                "fichier": "agent_simple_ia.py",
                "desc": "Analyse de texte basique"
            },
            "6": {
                "nom": "📡 Moniteur Réseau",
                "fichier": "moniteur_reseau.py",
                "desc": "Test de connexion et ports"
            },
            "7": {
                "nom": "🖥️ Dashboard Web",
                "fichier": "dashboard_web_agent.py",
                "desc": "Interface web sur port 8080"
            },
            "8": {
                "nom": "⚙️ Menu Commandes",
                "fichier": "menu_commandes.py",
                "desc": "Menu des commandes rapides"
            }
        }
    
    def afficher_banniere(self):
        os.system('clear')
        print("="*70)
        print("               🚀 SUITE COMPLÈTE DES AGENTS IA")
        print("="*70)
        print("📋 Sélectionnez un agent à lancer :")
        print()
    
    def verifier_dependances(self):
        """Vérifie et installe les dépendances si nécessaire"""
        try:
            import psutil
            print("✅ psutil est installé")
        except ImportError:
            print("📦 Installation de psutil...")
            subprocess.run([sys.executable, "-m", "pip", "install", "psutil", "--quiet"])
        
        try:
            import requests
            print("✅ requests est installé")
        except ImportError:
            print("📦 Installation de requests...")
            subprocess.run([sys.executable, "-m", "pip", "install", "requests", "--quiet"])
        
        try:
            import numpy
            print("✅ numpy est installé")
        except ImportError:
            print("📦 Installation de numpy...")
            subprocess.run([sys.executable, "-m", "pip", "install", "numpy", "--quiet"])
    
    def lancer_agent(self, fichier, nom):
        """Lance un agent"""
        if not os.path.exists(fichier):
            print(f"❌ Fichier {fichier} non trouvé")
            return False
        
        print(f"\n🚀 Lancement de {nom}...")
        print("="*50)
        
        try:
            result = subprocess.run([sys.executable, fichier])
            if result.returncode != 0:
                print(f"⚠️  Agent terminé avec code {result.returncode}")
            return True
        except KeyboardInterrupt:
            print("\n⏹️  Interruption par l'utilisateur")
            return True
        except Exception as e:
            print(f"❌ Erreur : {e}")
            return False
    
    def afficher_statut(self):
        """Affiche le statut des agents"""
        print("\n📊 STATUT DES AGENTS :")
        print("-"*40)
        
        agents_ok = 0
        for key, agent in self.agents.items():
            existe = os.path.exists(agent["fichier"])
            statut = "✅" if existe else "❌"
            print(f"{key}. {statut} {agent['nom']}")
            if existe:
                agents_ok += 1
        
        print(f"\n📈 {agents_ok}/{len(self.agents)} agents disponibles")
    
    def creer_agents_manquants(self):
        """Crée les agents manquants"""
        print("\n🛠️  Création des agents manquants...")
        
        agents_a_creer = []
        for agent in self.agents.values():
            if not os.path.exists(agent["fichier"]):
                agents_a_creer.append(agent["nom"])
        
        if not agents_a_creer:
            print("✅ Tous les agents sont déjà créés")
            return
        
        print(f"📝 Agents à créer : {len(agents_a_creer)}")
        for nom in agents_a_creer:
            print(f"  • {nom}")
        
        confirm = input("\nCréer ces agents ? (o/n) : ")
        if confirm.lower() == 'o':
            # Créer les fichiers de base
            for key, agent in self.agents.items():
                if not os.path.exists(agent["fichier"]):
                    with open(agent["fichier"], 'w') as f:
                        f.write(f'#!/usr/bin/env python3\nprint("{agent["nom"]} - En développement")')
                    os.chmod(agent["fichier"], 0o755)
                    print(f"✅ {agent['nom']} créé")
            
            print("\n✅ Création terminée !")
        else:
            print("❌ Création annulée")
    
    def main(self):
        while True:
            self.afficher_banniere()
            self.afficher_statut()
            
            print("\n" + "="*70)
            print("📋 MENU PRINCIPAL :")
            print("1-8. Lancer un agent spécifique")
            print("C.  Créer les agents manquants")
            print("D.  Vérifier les dépendances")
            print("L.  Lister tous les fichiers")
            print("S.  Système d'aide")
            print("0.  Quitter")
            print("="*70)
            
            choix = input("\n👉 Votre choix : ").upper()
            
            if choix == "0":
                print("\n👋 Au revoir ! Merci d'avoir utilisé la Suite Agents IA")
                break
            
            elif choix == "C":
                self.creer_agents_manquants()
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "D":
                print("\n🔍 Vérification des dépendances...")
                self.verifier_dependances()
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "L":
                print("\n📁 LISTE DES FICHIERS :")
                os.system("ls -la *.py | head -20")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "S":
                print("\n❓ AIDE :")
                print("• Choisissez un numéro (1-8) pour lancer un agent")
                print("• Appuyez sur Ctrl+C dans un agent pour revenir au menu")
                print("• Les agents créent automatiquement des logs et fichiers")
                print("• Utilisez 'C' pour créer les agents manquants")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix in self.agents:
                agent = self.agents[choix]
                self.lancer_agent(agent["fichier"], agent["nom"])
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            else:
                print("❌ Choix invalide")
                input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    suite = SuiteAgentsIA()
    suite.main()
EOF

# Rendre exécutable et lancer
chmod +x suite_agents_ia.py
python3 suite_agents_ia.py
