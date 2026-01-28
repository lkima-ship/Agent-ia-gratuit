# 1. Supprimez l'ancien fichier
rm /root/menu_unifie.py

# 2. Créez le fichier avec le code corrigé
cat > /root/menu_unifie.py << 'EOF'
#!/usr/bin/env python3
"""
🚀 MENU UNIFIE - Version Alpine
Scan automatique des agents Python
"""

import os
import sys
import subprocess
import glob

def clear_screen():
    """Efface l'écran"""
    os.system('clear')

def find_agents():
    """Trouve tous les agents Python"""
    print("🔍 Recherche des agents...")
    
    agents = []
    
    # Cherche dans les dossiers courants
    search_paths = [
        "/root",           # Dossier actuel
        "/root/agents",    # Dossier agents
        "/root/src",       # Dossier src
        "/root/*",         # Tous les sous-dossiers
        ".",               # Dossier courant
    ]
    
    for path in search_paths:
        try:
            # Cherche les fichiers .py
            for py_file in glob.glob(f"{path}/*.py"):
                filename = os.path.basename(py_file).lower()
                
                # Exclut les fichiers système
                if any(word in filename for word in ["menu", "test", "setup"]):
                    continue
                
                if os.path.isfile(py_file):
                    agents.append({
                        "name": os.path.basename(py_file),
                        "path": py_file,
                        "dir": os.path.dirname(py_file)
                    })
                    
            # Cherche récursivement dans certains dossiers
            if path in ["/root", "/root/src"]:
                for py_file in glob.glob(f"{path}/**/*.py", recursive=True):
                    filename = os.path.basename(py_file).lower()
                    if any(word in filename for word in ["menu", "test"]):
                        continue
                    if os.path.isfile(py_file):
                        agents.append({
                            "name": os.path.basename(py_file),
                            "path": py_file,
                            "dir": os.path.dirname(py_file)
                        })
        except:
            continue
    
    # Supprime les doublons
    unique_agents = []
    seen = set()
    for agent in agents:
        if agent["path"] not in seen:
            seen.add(agent["path"])
            unique_agents.append(agent)
    
    # Trie par nom
    unique_agents.sort(key=lambda x: x["name"])
    return unique_agents

def show_menu(agents):
    """Affiche le menu"""
    clear_screen()
    
    print("\n" + "="*50)
    print("🚀 MENU UNIFIE DES AGENTS")
    print("="*50)
    
    if not agents:
        print("\n❌ Aucun agent trouvé !")
        print("📁 Créez des fichiers .py dans /root/")
        return None, 0
    
    print(f"\n📊 {len(agents)} agents disponibles:\n")
    
    # Affiche les agents
    for i, agent in enumerate(agents, 1):
        print(f"{i:2}. {agent['name']:25} ({agent['dir']})")
    
    print("\n" + "-"*50)
    last_option = len(agents) + 1
    print(f"{last_option}. 🔄 Actualiser la liste")
    print(f"{last_option + 1}. ❌ Quitter")
    print("="*50)
    
    return agents, last_option + 1

def run_agent(agent):
    """Exécute un agent"""
    print(f"\n▶️  Lancement: {agent['name']}")
    print(f"📍 Chemin: {agent['path']}")
    print("-"*40)
    
    try:
        # Change de répertoire
        original_dir = os.getcwd()
        os.chdir(agent['dir'])
        
        # Exécute
        process = subprocess.Popen(
            [sys.executable, agent['name']],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Affiche la sortie en temps réel
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        
        # Retour au dossier original
        os.chdir(original_dir)
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\n⏎ Appuyez sur Entrée pour continuer...")

def main():
    """Fonction principale"""
    print("🚀 Menu Unifié - Chargement...")
    
    while True:
        # Trouve les agents
        agents = find_agents()
        
        # Affiche le menu
        agents_list, last_option = show_menu(agents)
        
        if agents_list is None:
            input("\n⏎ Appuyez sur Entrée pour réessayer...")
            continue
        
        # Demande le choix
        try:
            choix = input("\n👉 Votre choix: ").strip()
            
            if not choix:
                continue
            
            choix_num = int(choix)
            
            # Quitter
            if choix_num == last_option:
                print("\n👋 Au revoir !")
                break
            
            # Actualiser
            elif choix_num == last_option - 1:
                print("\n🔄 Actualisation...")
                continue
            
            # Exécuter un agent
            elif 1 <= choix_num <= len(agents_list):
                agent = agents_list[choix_num - 1]
                run_agent(agent)
            else:
                print("❌ Choix invalide !")
                input("\n⏎ Appuyez sur Entrée pour continuer...")
                
        except ValueError:
            print("❌ Veuillez entrer un nombre !")
            input("\n⏎ Appuyez sur Entrée pour continuer...")
        except KeyboardInterrupt:
            print("\n\n👋 Interruption - Au revoir !")
            break

if __name__ == "__main__":
    main()
EOF
