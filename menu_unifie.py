#!/usr/bin/env python3
"""
MENU UNIFIE DES AGENTS
Scanne automatiquement tous les dossiers pour trouver les agents Python
"""

import os
import sys
import subprocess
from pathlib import Path

class AgentManager:
    def __init__(self):
        self.home_dir = Path.home()
        self.current_dir = Path.cwd()
        self.agents = {}
        self.categories = {}
        
    def find_agents(self):
        """Recherche récursive tous les fichiers Python agents"""
        # Dossiers à scanner (ajoutez les vôtres)
        search_dirs = [
            self.current_dir,
            self.home_dir,
            self.home_dir / "Desktop",
            self.home_dir / "Documents",
            self.home_dir / "agents",
            self.home_dir / "src",
            self.home_dir / "modules",
            Path("/root"),  # Si vous travaillez en root
        ]
        
        # Fichiers à exclure (menus, tests, etc.)
        exclude_files = [
            "menu", "test", "__init__", "setup", "requirements",
            "start", "run", "launch", "install", "docker", "api"
        ]
        
        print("🔍 Scan des agents en cours...")
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            try:
                # Parcours récursif
                for py_file in search_dir.rglob("*.py"):
                    # Vérifie si c'est un agent (exclut les fichiers système)
                    filename = py_file.stem.lower()
                    
                    # Exclusion basée sur le nom
                    if any(exclude in filename for exclude in exclude_files):
                        continue
                    
                    # Vérifie si le fichier contient du code Python valide
                    if self.is_valid_agent(py_file):
                        # Catégorie basée sur le dossier parent
                        category = py_file.parent.name
                        if not category or category == ".":
                            category = "Divers"
                        
                        # Ajoute à la liste
                        if category not in self.agents:
                            self.agents[category] = []
                        
                        self.agents[category].append({
                            "name": py_file.name,
                            "path": py_file,
                            "size": py_file.stat().st_size,
                            "modified": py_file.stat().st_mtime
                        })
                        
            except PermissionError:
                continue
        
        # Trie les agents par nom dans chaque catégorie
        for category in self.agents:
            self.agents[category].sort(key=lambda x: x["name"])
        
        return len(self.agents) > 0
    
    def is_valid_agent(self, file_path):
        """Vérifie si le fichier semble être un agent valide"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(500)  # Lit les 500 premiers caractères
                
                # Vérifications simples
                if not content.strip():
                    return False
                    
                # Doit contenir au moins une des chaînes suivantes
                indicators = [
                    "def ", "class ", "import ", "print(", "input(",
                    "agent", "main()", "if __name__"
                ]
                
                return any(indicator in content for indicator in indicators)
        except:
            return False
    
    def display_menu(self):
        """Affiche le menu principal"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        print("\n" + "="*60)
        print("🚀 MENU UNIFIE DES AGENTS - TOUS VOS AGENTS EN UN CLIC")
        print("="*60)
        
        total_agents = sum(len(agents) for agents in self.agents.values())
        print(f"\n📊 {total_agents} agents trouvés dans {len(self.agents)} catégories\n")
        
        # Affiche les catégories avec agents
        category_index = 1
        self.category_map = {}
        
        for category, agents in sorted(self.agents.items()):
            self.category_map[category_index] = category
            print(f"{category_index}. 📁 {category} ({len(agents)} agents)")
            category_index += 1
        
        print("\n" + "-"*60)
        print(f"{category_index}. 🔄 Rescan des agents")
        print(f"{category_index + 1}. 📂 Ouvrir le dossier des agents")
        print(f"{category_index + 2}. ❌ Quitter")
        print("="*60)
        
        return category_index + 2  # Dernier index
    
    def display_category(self, category):
        """Affiche les agents d'une catégorie"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        agents = self.agents[category]
        
        print(f"\n📁 CATEGORIE: {category}")
        print("="*60)
        
        agent_index = 1
        self.agent_map = {}
        
        for agent in agents:
            self.agent_map[agent_index] = agent
            size_kb = agent["size"] / 1024
            print(f"{agent_index:2}. 📄 {agent['name']:30} ({size_kb:.1f} KB)")
            agent_index += 1
        
        print("\n" + "-"*60)
        print(f"{agent_index}. ↩️ Retour au menu principal")
        print("="*60)
        
        return agent_index
    
    def run_agent(self, agent_info):
        """Exécute l'agent sélectionné"""
        print(f"\n▶️  Lancement de: {agent_info['name']}")
        print(f"📍 Chemin: {agent_info['path']}")
        print("-"*40)
        
        try:
            # Change le répertoire courant vers celui de l'agent
            original_dir = os.getcwd()
            os.chdir(agent_info['path'].parent)
            
            # Exécute l'agent
            subprocess.run([sys.executable, agent_info['path'].name], check=True)
            
            # Retour au répertoire original
            os.chdir(original_dir)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'exécution: {e}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        finally:
            input("\n⏎ Appuyez sur Entrée pour continuer...")
    
    def open_agents_folder(self):
        """Ouvre le dossier contenant les agents"""
        if os.name == 'posix':  # Linux/Mac
            # Crée un dossier agents s'il n'existe pas
            agents_dir = self.home_dir / "agents"
            agents_dir.mkdir(exist_ok=True)
            
            # Ouvre le dossier
            subprocess.run(["xdg-open", str(agents_dir)])
        else:  # Windows
            os.startfile(str(self.home_dir / "agents"))
        
        print("📂 Dossier agents ouvert!")
        input("\n⏎ Appuyez sur Entrée pour continuer...")

def main():
    manager = AgentManager()
    
    while True:
        # Trouve les agents
        if not manager.find_agents():
            print("❌ Aucun agent trouvé!")
            print("📁 Créez un dossier 'agents' dans votre home et placez-y vos scripts.")
            input("⏎ Appuyez sur Entrée pour réessayer...")
            continue
        
        # Affiche le menu principal
        last_index = manager.display_menu()
        
        try:
            choix = input("\n👉 Votre choix: ").strip()
            
            if not choix:
                continue
                
            choix_num = int(choix)
            
            # Quitter
            if choix_num == last_index:
                print("\n👋 Au revoir!")
                break
                
            # Rescan
            elif choix_num == last_index - 2:
                print("\n🔄 Rescan en cours...")
                continue
                
            # Ouvrir dossier
            elif choix_num == last_index - 1:
                manager.open_agents_folder()
                continue
                
            # Catégorie sélectionnée
            elif 1 <= choix_num <= len(manager.agents):
                category = manager.category_map[choix_num]
                
                # Boucle dans la catégorie
                while True:
                    last_agent_index = manager.display_category(category)
                    
                    choix_agent = input("\n👉 Choisissez un agent (ou 'r' pour retour): ").strip()
                    
                    if choix_agent.lower() == 'r':
                        break
                    
                    try:
                        choix_agent_num = int(choix_agent)
                        
                        if 1 <= choix_agent_num <= len(manager.agents[category]):
                            agent = manager.agent_map[choix_agent_num]
                            manager.run_agent(agent)
                        elif choix_agent_num == last_agent_index:
                            break
                        else:
                            print("❌ Choix invalide!")
                            input("⏎ Appuyez sur Entrée pour continuer...")
                            
                    except ValueError:
                        print("❌ Veuillez entrer un nombre!")
                        input("⏎ Appuyez sur Entrée pour continuer...")
                        
            else:
                print("❌ Choix invalide!")
                input("⏎ Appuyez sur Entrée pour continuer...")
                
        except ValueError:
            print("❌ Veuillez entrer un nombre valide!")
            input("⏎ Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            print("\n\n👋 Interruption - Au revoir!")
            break

if __name__ == "__main__":
    # Vérifie Python 3
    if sys.version_info < (3, 6):
        print("❌ Python 3.6 ou supérieur requis!")
        sys.exit(1)
    
    # Lance le menu
    main()
