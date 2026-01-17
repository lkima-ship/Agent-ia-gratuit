# Créer le menu principal unifié
cat > /root/menu_principal.py << 'EOF'
#!/usr/bin/env python3
"""
🎛️ MENU PRINCIPAL UNIFIÉ - Tous les agents IA
Système intelligent de détection et lancement
"""
import os
import sys
import json
import subprocess
import time
from datetime import datetime
import threading

class AgentManager:
    """Gestionnaire intelligent d'agents"""
    
    def __init__(self):
        self.agents_dir = "/root"
        self.agents_data = "/root/agents_config.json"
        self.detected_agents = []
        self.categories = {}
        self.load_agents()
    
    def load_agents(self):
        """Charge et détecte automatiquement tous les agents"""
        print("🔍 Détection des agents en cours...")
        
        # Catégories d'agents avec leurs caractéristiques
        categories = {
            "intelligence": ["cognitif", "ia", "intelligent", "brain", "ml"],
            "web": ["web", "interface", "browser", "scraping", "http"],
            "analyse": ["analyse", "data", "donnees", "stats", "analytics"],
            "surveillance": ["surveillance", "monitor", "watch", "log"],
            "systeme": ["system", "sys", "hub", "manager", "menu"],
            "communication": ["chat", "bot", "assistant", "agent"]
        }
        
        # Scanner tous les fichiers Python
        for file in os.listdir(self.agents_dir):
            if file.endswith(".py") and not file.startswith("__"):
                file_path = os.path.join(self.agents_dir, file)
                
                # Lire la première ligne pour détecter le type
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(500).lower()
                        
                    # Déterminer la catégorie
                    category = "divers"
                    for cat, keywords in categories.items():
                        if any(keyword in content.lower() or keyword in file.lower() for keyword in keywords):
                            category = cat
                            break
                    
                    # Déterminer le type d'agent
                    agent_type = "executable"
                    if "interface" in file.lower() or "web" in file.lower():
                        agent_type = "web"
                    elif "menu" in file.lower() or "principal" in file.lower():
                        agent_type = "menu"
                    elif "cognitif" in file.lower():
                        agent_type = "ia_avancee"
                    
                    # Vérifier si c'est exécutable
                    executable = os.access(file_path, os.X_OK)
                    
                    # Taille du fichier
                    size = os.path.getsize(file_path)
                    
                    # Description automatique
                    description = self.auto_describe(file, content)
                    
                    agent_info = {
                        "nom": file,
                        "nom_affichage": file.replace(".py", "").replace("_", " ").title(),
                        "chemin": file_path,
                        "categorie": category,
                        "type": agent_type,
                        "executable": executable,
                        "taille": size,
                        "description": description,
                        "statut": "✅" if executable and size > 100 else "⚠️",
                        "derniere_execution": None
                    }
                    
                    self.detected_agents.append(agent_info)
                    
                    # Ajouter à la catégorie
                    if category not in self.categories:
                        self.categories[category] = []
                    self.categories[category].append(agent_info)
                    
                except Exception as e:
                    print(f"⚠️  Erreur lecture {file}: {e}")
        
        # Trier les agents
        self.detected_agents.sort(key=lambda x: x["nom"])
        print(f"✅ {len(self.detected_agents)} agents détectés")
    
    def auto_describe(self, filename, content):
        """Génère automatiquement une description"""
        filename_lower = filename.lower()
        
        descriptions = {
            "web": "Interface web et outils de navigation",
            "ia": "Intelligence artificielle et machine learning",
            "cognitif": "Agent cognitif avec mémoire et apprentissage",
            "analyse": "Analyse de données et statistiques",
            "surveillance": "Monitoring système et sécurité",
            "menu": "Interface de navigation et contrôle",
            "agent": "Agent autonome avec spécialisation",
            "hub": "Centre de contrôle et coordination",
            "interface": "Interface utilisateur",
            "donnees": "Gestion et analyse de données"
        }
        
        # Chercher des mots-clés
        for key, desc in descriptions.items():
            if key in filename_lower:
                return desc
        
        # Détection par contenu
        if "http.server" in content:
            return "Serveur web et interface HTTP"
        elif "import requests" in content:
            return "Outils web et requêtes HTTP"
        elif "sqlite" in content or "database" in content:
            return "Base de données et stockage"
        elif "scraping" in content or "beautifulsoup" in content:
            return "Scraping web et extraction de données"
        elif "machine learning" in content or "ml" in content:
            return "Machine Learning et intelligence artificielle"
        elif "surveillance" in content or "monitor" in content:
            return "Surveillance système en temps réel"
        
        return "Agent Python avec fonctionnalités spécialisées"
    
    def afficher_menu(self):
        """Affiche le menu principal avec tous les agents"""
        print("\n" + "="*80)
        print("                    🤖 SYSTÈME UNIFIÉ D'AGENTS IA")
        print("="*80)
        
        # Afficher par catégories
        for category, agents in self.categories.items():
            emoji = self.get_category_emoji(category)
            print(f"\n{emoji} {category.upper()} ({len(agents)} agents) :")
            print("-" * 40)
            
            for i, agent in enumerate(agents, 1):
                num = len([a for a in self.detected_agents if a["categorie"] == category and self.detected_agents.index(a) < self.detected_agents.index(agent)]) + 1
                print(f"{agent['statut']} {num:2d}. {agent['nom_affichage']:30} → {agent['description'][:40]}...")
    
    def get_category_emoji(self, category):
        """Retourne un emoji pour chaque catégorie"""
        emojis = {
            "intelligence": "🧠",
            "web": "🌐",
            "analyse": "📊",
            "surveillance": "👁️",
            "systeme": "⚙️",
            "communication": "💬",
            "divers": "📁"
        }
        return emojis.get(category, "📄")
    
    def lancer_agent(self, agent_index):
        """Lance un agent spécifique"""
        if 0 <= agent_index < len(self.detected_agents):
            agent = self.detected_agents[agent_index]
            print(f"\n🚀 Lancement de : {agent['nom_affichage']}")
            print(f"📁 Fichier : {agent['nom']}")
            print(f"📝 Description : {agent['description']}")
            print(f"⚙️  Type : {agent['type']}")
            print("-" * 60)
            
            try:
                # Enregistrer l'exécution
                agent["derniere_execution"] = datetime.now().isoformat()
                
                # Lancer l'agent
                if agent["type"] == "web":
                    print(f"🌐 Interface web sur : http://localhost:8080")
                    print("🛑 Arrêt : Ctrl+C")
                
                # Exécuter le script
                subprocess.run([sys.executable, agent["chemin"]])
                
                return True
            except Exception as e:
                print(f"❌ Erreur : {e}")
                return False
        else:
            print("❌ Index d'agent invalide")
            return False
    
    def afficher_info_agent(self, agent_index):
        """Affiche les informations détaillées d'un agent"""
        if 0 <= agent_index < len(self.detected_agents):
            agent = self.detected_agents[agent_index]
            
            print("\n" + "="*60)
            print(f"📋 INFORMATIONS COMPLÈTES - {agent['nom_affichage']}")
            print("="*60)
            print(f"📁 Fichier : {agent['nom']}")
            print(f"📂 Chemin : {agent['chemin']}")
            print(f"📝 Description : {agent['description']}")
            print(f"🏷️  Catégorie : {agent['categorie']}")
            print(f"⚙️  Type : {agent['type']}")
            print(f"📏 Taille : {agent['taille']} octets")
            print(f"✅ Exécutable : {'Oui' if agent['executable'] else 'Non'}")
            print(f"🔄 Dernière exécution : {agent['derniere_execution'] or 'Jamais'}")
            
            # Afficher un aperçu du contenu
            print(f"\n📄 APERÇU DU CODE (premières 5 lignes) :")
            try:
                with open(agent["chemin"], 'r', encoding='utf-8', errors='ignore') as f:
                    for i in range(5):
                        line = f.readline().strip()
                        if line:
                            print(f"   {line[:80]}")
            except:
                print("   Impossible de lire le fichier")
            
            return True
        return False
    
    def rechercher_agents(self, terme):
        """Recherche des agents par terme"""
        resultats = []
        terme_lower = terme.lower()
        
        for agent in self.detected_agents:
            if (terme_lower in agent["nom"].lower() or 
                terme_lower in agent["description"].lower() or
                terme_lower in agent["categorie"].lower()):
                resultats.append(agent)
        
        return resultats
    
    def exporter_liste(self):
        """Exporte la liste des agents"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/root/agents_liste_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.detected_agents, f, indent=2, ensure_ascii=False, default=str)
        
        return filename

def menu_interactif():
    """Interface utilisateur interactive"""
    manager = AgentManager()
    
    # Démarrer un thread pour la détection en arrière-plan
    def background_detection():
        while True:
            time.sleep(30)
            old_count = len(manager.detected_agents)
            manager.load_agents()
            new_count = len(manager.detected_agents)
            if new_count != old_count:
                print(f"\n🔄 {new_count - old_count} nouveaux agents détectés")
    
    detection_thread = threading.Thread(target=background_detection, daemon=True)
    detection_thread.start()
    
    while True:
        print("\n" + "="*80)
        print("                    🎛️  MENU PRINCIPAL DES AGENTS")
        print("="*80)
        print(f"📊 Total agents : {len(manager.detected_agents)} | Catégories : {len(manager.categories)}")
        print("\n📋 OPTIONS PRINCIPALES :")
        print("1. 📜 Lister tous les agents par catégorie")
        print("2. 🚀 Lancer un agent spécifique")
        print("3. 🔍 Rechercher un agent")
        print("4. 📊 Voir les statistiques")
        print("5. ⚙️  Gérer les agents")
        print("6. 💾 Exporter la liste des agents")
        print("7. 🔄 Re-détecter les agents")
        print("0. 🚪 Quitter")
        
        try:
            choix = input("\n👉 Votre choix : ").strip()
            
            if choix == "1":
                manager.afficher_menu()
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "2":
                print("\n🎯 LANCEMENT D'AGENT")
                manager.afficher_menu()
                
                try:
                    index = int(input("\n📝 Numéro de l'agent à lancer : ")) - 1
                    if manager.lancer_agent(index):
                        print("\n✅ Agent lancé avec succès")
                    else:
                        print("\n❌ Échec du lancement")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "3":
                print("\n🔍 RECHERCHE D'AGENTS")
                terme = input("Mot-clé à rechercher : ").strip()
                if terme:
                    resultats = manager.rechercher_agents(terme)
                    print(f"\n📊 {len(resultats)} résultat(s) trouvé(s) pour '{terme}' :")
                    for i, agent in enumerate(resultats, 1):
                        print(f"{i}. {agent['nom_affichage']} - {agent['description']}")
                else:
                    print("❌ Terme de recherche vide")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "4":
                print("\n📊 STATISTIQUES DU SYSTÈME")
                print(f"Total agents : {len(manager.detected_agents)}")
                print("Par catégorie :")
                for categorie, agents in manager.categories.items():
                    print(f"  {manager.get_category_emoji(categorie)} {categorie} : {len(agents)} agents")
                
                # Agents exécutables
                executables = sum(1 for a in manager.detected_agents if a["executable"])
                print(f"\n✅ Agents exécutables : {executables}/{len(manager.detected_agents)}")
                
                # Taille totale
                taille_totale = sum(a["taille"] for a in manager.detected_agents)
                print(f"📏 Taille totale : {taille_totale/1024:.1f} KB")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "5":
                print("\n⚙️  GESTION DES AGENTS")
                print("1. 🔧 Rendre tous les agents exécutables")
                print("2. 📋 Voir les détails d'un agent")
                print("3. 🗑️  Supprimer un agent")
                print("4. 📝 Éditer un agent")
                print("0. ↩️ Retour")
                
                sous_choix = input("\nChoix de gestion : ").strip()
                
                if sous_choix == "1":
                    print("\n🔧 Rendre tous les agents exécutables...")
                    for agent in manager.detected_agents:
                        try:
                            os.chmod(agent["chemin"], 0o755)
                            print(f"✅ {agent['nom']} rendu exécutable")
                        except:
                            print(f"❌ Impossible de modifier {agent['nom']}")
                
                elif sous_choix == "2":
                    manager.afficher_menu()
                    try:
                        index = int(input("\nNuméro de l'agent à inspecter : ")) - 1
                        manager.afficher_info_agent(index)
                    except ValueError:
                        print("❌ Numéro invalide")
                
                elif sous_choix == "3":
                    manager.afficher_menu()
                    try:
                        index = int(input("\nNuméro de l'agent à supprimer : ")) - 1
                        if 0 <= index < len(manager.detected_agents):
                            agent = manager.detected_agents[index]
                            confirm = input(f"Confirmer la suppression de {agent['nom']} ? (o/n) : ")
                            if confirm.lower() == 'o':
                                os.remove(agent["chemin"])
                                print(f"🗑️  {agent['nom']} supprimé")
                                manager.load_agents()
                    except Exception as e:
                        print(f"❌ Erreur : {e}")
                
                elif sous_choix == "4":
                    print("\n📝 ÉDITION D'AGENT")
                    print("Utilisez la commande : nano /root/nom_agent.py")
                    print("Ou : python3 -c \"print('Édition via Python')\"")
                    input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "6":
                print("\n💾 EXPORTATION DE LA LISTE")
                fichier = manager.exporter_liste()
                print(f"✅ Liste exportée dans : {fichier}")
                print(f"📊 {len(manager.detected_agents)} agents exportés")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "7":
                print("\n🔄 RE-DÉTECTION DES AGENTS")
                old_count = len(manager.detected_agents)
                manager.load_agents()
                new_count = len(manager.detected_agents)
                print(f"✅ Détection terminée : {new_count} agents")
                if new_count > old_count:
                    print(f"✨ {new_count - old_count} nouveaux agents détectés !")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            
            elif choix == "0":
                print("\n👋 Au revoir !")
                print(f"📚 Session terminée - {len(manager.detected_agents)} agents disponibles")
                break
            
            else:
                print("❌ Choix invalide")
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption par l'utilisateur")
            continue
        except Exception as e:
            print(f"\n❌ Erreur : {e}")

if __name__ == "__main__":
    # Vérifier les dépendances
    try:
        import sqlite3
    except ImportError:
        print("📦 Installation de sqlite3...")
        os.system("apk add sqlite 2>/dev/null || echo 'SQLite déjà installé'")
    
    print("🚀 Initialisation du système d'agents...")
    menu_interactif()
EOF

# Rendre exécutable
chmod +x /root/menu_principal.py
