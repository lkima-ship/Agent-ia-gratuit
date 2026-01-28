#!/usr/bin/env python3
"""
SYSTÈME IA - MENU PRINCIPAL
Version complète avec toutes les fonctionnalités
"""

import os
import sys
import subprocess
import time

# Configuration des dossiers
AGENTS_DIR = "agents"  # ou "AGENTS" selon votre structure
APIS_DIR = "apis"
SCRIPTS_DIR = "scripts"
WEB_DIR = "web"

# Fonction pour effacer l'écran
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour scanner les fichiers d'un dossier
def scan_directory(directory, extensions=None):
    fichiers = []
    count = 0
    
    if os.path.exists(directory):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                if extensions:
                    if any(item.lower().endswith(ext.lower()) for ext in extensions):
                        fichiers.append(item)
                        count += 1
                else:
                    fichiers.append(item)
                    count += 1
    
    return fichiers, count

# Fonction pour afficher une liste de fichiers
def afficher_liste_fichiers(fichiers, categorie, limite=20):
    clear_screen()
    print("\n" + "=" * 40 + "\n")
    print(f"📂 {categorie.upper()} ({len(fichiers)} fichiers)\n")
    
    if not fichiers:
        print("Aucun fichier trouvé.")
    else:
        for i, fichier in enumerate(fichiers[:limite], 1):
            print(f"{i}. {fichier}")
        
        if len(fichiers) > limite:
            print(f"\n... et {len(fichiers) - limite} autres fichiers")
    
    input("\nAppuyez sur Entrée pour continuer...")

# Fonction pour lancer un agent
def lancer_agent():
    clear_screen()
    
    # Chercher les agents IA
    agents_py = []
    
    # D'abord dans le dossier agents
    if os.path.exists(AGENTS_DIR):
        for f in os.listdir(AGENTS_DIR):
            if f.endswith('.py') and 'agent' in f.lower():
                agents_py.append(os.path.join(AGENTS_DIR, f))
    
    # Ensuite dans le répertoire courant
    for f in os.listdir('.'):
        if f.endswith('.py') and 'agent' in f.lower() and f not in [os.path.basename(a) for a in agents_py]:
            agents_py.append(f)
    
    if not agents_py:
        print("❌ Aucun agent IA trouvé.")
        print("\nLes agents doivent être des fichiers Python avec 'agent' dans le nom.")
        input("\nAppuyez sur Entrée pour continuer...")
        return
    
    print("\n" + "=" * 40)
    print("🚀 LANCER UN AGENT IA")
    print("=" * 40 + "\n")
    
    print("📋 Liste des agents disponibles:\n")
    for i, agent in enumerate(agents_py, 1):
        print(f"{i}. {os.path.basename(agent)}")
    
    print(f"\n{len(agents_py)} agent(s) disponible(s)")
    
    try:
        choix = input("\nNuméro de l'agent à lancer (0 pour annuler): ")
        if choix == "0":
            return
        
        index = int(choix) - 1
        if 0 <= index < len(agents_py):
            agent_path = agents_py[index]
            print(f"\n▶️  Lancement de {os.path.basename(agent_path)}...")
            
            # Lancer l'agent dans un sous-processus
            try:
                subprocess.run([sys.executable, agent_path], check=True)
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur lors de l'exécution: {e}")
            except KeyboardInterrupt:
                print("\n⏹️  Arrêt de l'agent...")
            
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("❌ Choix invalide.")
            time.sleep(1)
    except ValueError:
        print("❌ Veuillez entrer un nombre valide.")
        time.sleep(1)

# Menu principal
def menu_principal():
    while True:
        clear_screen()
        
        # Scanner les différents types de fichiers
        agents, count_agents = scan_directory(AGENTS_DIR, ['.py'])
        apis, count_apis = scan_directory(APIS_DIR, ['.py'])
        scripts, count_scripts = scan_directory(SCRIPTS_DIR, ['.py'])
        sites_web, count_web = scan_directory(WEB_DIR, ['.html', '.htm'])
        
        # Compter aussi les fichiers dans le répertoire courant
        if not os.path.exists(AGENTS_DIR):
            # Si le dossier n'existe pas, chercher les agents dans le répertoire courant
            for f in os.listdir('.'):
                if f.endswith('.py') and 'agent' in f.lower():
                    agents.append(f)
                    count_agents += 1
        
        print("\n" + "=" * 40 + "\n")
        print("🤖 SYSTÈME IA - MENU PRINCIPAL\n")
        print("VOTRE SYSTÈME CONTIENT:")
        print(f"  🤖 Agents IA: {count_agents} fichiers")
        print(f"  🌐 APIs: {count_apis} fichiers")
        print(f"  📜 Scripts: {count_scripts} fichiers")
        print(f"  🖥️  Sites Web: {count_web} fichiers")
        print("\n" + "-" * 40 + "\n")
        
        print("📋 MENU:")
        print("1. 🤖 Voir mes agents IA")
        print("2. 🚀 Lancer un agent")
        print("3. 🌐 Voir mes APIs")
        print("4. 📜 Voir mes scripts")
        print("5. 🖥️  Voir mes sites web")
        print("6. ❌ Quitter")
        print("\n" + "-" * 40 + "\n")
        
        choix = input("Votre choix (1-6): ").strip()
        
        if choix == "1":
            afficher_liste_fichiers(agents, "AGENTS IA")
        elif choix == "2":
            lancer_agent()
        elif choix == "3":
            afficher_liste_fichiers(apis, "APIs")
        elif choix == "4":
            afficher_liste_fichiers(scripts, "SCRIPTS")
        elif choix == "5":
            afficher_liste_fichiers(sites_web, "SITES WEB")
        elif choix == "6":
            print("\n👋 Au revoir !")
            time.sleep(1)
            clear_screen()
            break
        else:
            print("\n❌ Choix invalide. Veuillez choisir entre 1 et 6.")
            time.sleep(1)

# Version alternative simple (comme dans la capture)
def menu_simple():
    """Version simple sans scan de dossiers - utilise les comptes fixes"""
    while True:
        clear_screen()
        
        print("\n" + "=" * 40 + "\n")
        print("SYSTÈME IA - MENU PRINCIPAL\n")
        print("VOTRE SYSTÈME CONTIENT:")
        print("Agents IA: 18 fichiers")
        print("APIs: 10 fichiers")
        print("Scripts: 30 fichiers")
        print("Sites Web: 9 fichiers")
        print("\n---\n")
        print("MENU:")
        print("1. 🐍 Voir mes agents IA")
        print("2. 📄 Lancer un agent")
        print("3. 💻 Voir mes APIs")
        print("4. 📝 Voir mes scripts")
        print("5. 🔧 Voir mes sites web")
        print("6. ❌ Quitter")
        print("\n---\n")
        
        choix = input("Votre choix (1-6): ").strip()
        
        if choix == "1":
            # Liste des agents comme dans la capture
            agents = [
                "web_dashboard_v2.py", "nom_fichier.py", "moniteur_reseau.py",
                "index_agents.py", "api_agents_complete.py", "install_deps.py",
                "garantie.py", "organiseur_intelligent.py", "simple_menu.py",
                "simple_working.py", "organiser_fichiers.py", "suite_agents_ia.py",
                "mon_nouvel_agent.py", "assistant_personnel.py", "hub_agents.py",
                "organize_files.py", "analyseur_fichiers.py", "smart_organize.py"
            ]
            
            clear_screen()
            for i, agent in enumerate(agents, 1):
                print(f"{i}. {agent}")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "2":
            lancer_agent()
            
        elif choix == "3":
            # Liste des APIs
            apis = [
                "api_agents_complete.py", "api_dashboard.py", "api_system.py",
                "api_monitoring.py", "api_organizer.py", "api_web.py",
                "api_database.py", "api_ml.py", "api_vision.py", "api_nlp.py"
            ]
            
            clear_screen()
            print("- [x] VOS APIs:")
            for api in apis:
                print(f"  - {api}")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "4":
            # Liste des scripts
            scripts = [f"script_{i}.py" for i in range(1, 31)]
            
            clear_screen()
            print("- [x] VOS SCRIPTS:")
            for i in range(0, 30, 5):
                print("  " + ", ".join(scripts[i:i+5]))
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "5":
            # Liste des sites web
            sites = [
                "boutique_iphone.html", "index.html", "ma_boutique.fr.html",
                "boutique_finale.html", "#_liste_des_fichiers_api_disponibles.html",
                "maboutique.html", "test.html", "index_structure.html",
                "boutique_finale.htm"
            ]
            
            clear_screen()
            print("- [x] VOS SITES WEB:")
            for site in sites:
                print(f"  - {site}")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "6":
            print("\nAu revoir !")
            time.sleep(1)
            clear_screen()
            break
        else:
            print("\nChoix invalide !")
            time.sleep(1)

if __name__ == "__main__":
    # Choisir la version du menu
    print("Choisissez la version du menu:")
    print("1. Menu dynamique (scan des dossiers)")
    print("2. Menu statique (comme dans les captures)")
    
    version = input("Votre choix (1-2): ").strip()
    
    if version == "1":
        menu_principal()
    else:
        menu_simple()
