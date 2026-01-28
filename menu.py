#!/usr/bin/env python3
"""
SYSTÈME IA - MENU PRINCIPAL
Version simple et fonctionnelle
"""

import os
import time
import subprocess

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_agents():
    """Affiche la liste des agents"""
    clear_screen()
    agents = [
        "web_dashboard_v2.py", "nom_fichier.py", "moniteur_reseau.py",
        "index_agents.py", "api_agents_complete.py", "install_deps.py",
        "garantie.py", "organiseur_intelligent.py", "simple_menu.py",
        "simple_working.py", "organiser_fichiers.py", "suite_agents_ia.py",
        "mon_nouvel_agent.py", "assistant_personnel.py", "hub_agents.py",
        "organize_files.py", "analyseur_fichiers.py", "smart_organize.py"
    ]
    
    print("\n" + "=" * 40)
    print("🤖 AGENTS IA DISPONIBLES")
    print("=" * 40 + "\n")
    
    for i, agent in enumerate(agents, 1):
        print(f"{i:2}. {agent}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def launch_agent():
    """Lance un agent spécifique"""
    clear_screen()
    print("\n🚀 LANCER UN AGENT")
    print("=" * 40 + "\n")
    
    agents = [
        "web_dashboard_v2.py", "nom_fichier.py", "moniteur_reseau.py",
        "index_agents.py", "api_agents_complete.py", "install_deps.py",
        "garantie.py", "organiseur_intelligent.py", "simple_menu.py",
        "simple_working.py", "organiser_fichiers.py", "suite_agents_ia.py",
        "mon_nouvel_agent.py", "assistant_personnel.py", "hub_agents.py",
        "organize_files.py", "analyseur_fichiers.py", "smart_organize.py"
    ]
    
    for i, agent in enumerate(agents, 1):
        print(f"{i:2}. {agent}")
    
    try:
        choice = input("\nNuméro de l'agent: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(agents):
                agent_file = agents[idx]
                print(f"\n⚠️ Lancement de {agent_file}...")
                
                # Vérifier si le fichier existe
                if not os.path.exists(agent_file):
                    print(f"❌ Le fichier {agent_file} n'existe pas.")
                else:
                    # Exécuter l'agent
                    try:
                        subprocess.run(['python3', agent_file])
                    except Exception as e:
                        print(f"❌ Erreur d'exécution: {e}")
            else:
                print("❌ Numéro invalide")
        else:
            print("❌ Veuillez entrer un nombre")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\n↪ Appuyez sur Entrée pour continuer...")

def main():
    """Menu principal"""
    while True:
        clear_screen()
        print("\n" + "=" * 40)
        print("🤖 SYSTÈME IA - MENU PRINCIPAL")
        print("=" * 40 + "\n")
        
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
            show_agents()
        elif choix == "2":
            launch_agent()
        elif choix == "3":
            print("\n💻 APIs disponibles:")
            print("- api_agents_complete.py")
            print("- api_dashboard.py")
            print("- api_system.py")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "4":
            print("\n📝 Scripts disponibles:")
            print("- moniteur_systeme.py")
            print("- organiser_final.py")
            print("- dashboard_web.py")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "5":
            print("\n🔧 Sites Web disponibles:")
            print("- index.html")
            print("- boutique_iphone.html")
            print("- ma_boutique.fr.html")
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "6":
            print("\n👋 Au revoir !")
            time.sleep(1)
            break
        else:
            print("\n❌ Choix invalide !")
            time.sleep(1)

if __name__ == "__main__":
    main()
