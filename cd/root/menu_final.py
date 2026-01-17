cat > /root/menu_final.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def show_stats():
    clear_screen()
    print("╔══════════════════════════════════════╗")
    print("║        STATISTIQUES SYSTÈME         ║")
    print("╚══════════════════════════════════════╝")
    
    all_py = [f for f in os.listdir("/root") if f.endswith(".py")]
    agents = [f for f in all_py if f.startswith("agent_")]
    menus = [f for f in all_py if "menu" in f.lower()]
    interfaces = [f for f in all_py if "interface" in f.lower()]
    dashboards = [f for f in all_py if "dashboard" in f.lower()]
    apis = [f for f in all_py if "api" in f.lower()]
    
    print(f"\n📊 Fichiers Python: {len(all_py)}")
    print(f"🚀 Agents IA: {len(agents)}")
    print(f"📋 Menus: {len(menus)}")
    print(f"🖥️  Interfaces: {len(interfaces)}")
    print(f"📈 Dashboards: {len(dashboards)}")
    print(f"🔌 APIs: {len(apis)}")
    
    print(f"\n💾 Espace disque:")
    os.system("df -h / | tail -1")
    
    print(f"\n🐍 Python: {sys.version.split()[0]}")
    
    input("\n↵ Appuyez sur Entrée pour continuer...")

def list_agents():
    clear_screen()
    print("╔══════════════════════════════════════╗")
    print("║        LISTE DES AGENTS             ║")
    print("╚══════════════════════════════════════╝")
    
    agents = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
    
    if not agents:
        print("\n❌ Aucun agent trouvé!")
        input("\n↵ Appuyez sur Entrée pour continuer...")
        return
    
    print(f"\n📋 Total: {len(agents)} agents\n")
    
    # Afficher par groupes de 10
    for i in range(0, len(agents), 10):
        print("─" * 40)
        for j, agent in enumerate(agents[i:i+10], i+1):
            print(f"{j:3d}. {agent}")
    
    print("\n" + "═" * 40)
    
    print("\nOptions:")
    print("  1. Lancer un agent")
    print("  2. Retour au menu")
    
    choix = input("\nVotre choix: ")
    
    if choix == "1":
        launch_agent(agents)
    elif choix == "2":
        return

def launch_agent(agents_list=None):
    clear_screen()
    print("╔══════════════════════════════════════╗")
    print("║        LANCEUR D'AGENTS             ║")
    print("╚══════════════════════════════════════╝")
    
    if agents_list is None:
        agents_list = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
    
    if not agents_list:
        print("\n❌ Aucun agent trouvé!")
        input("\n↵ Appuyez sur Entrée pour continuer...")
        return
    
    print(f"\n🔧 {len(agents_list)} agents disponibles\n")
    
    # Afficher les premiers agents
    for i, agent in enumerate(agents_list[:15], 1):
        print(f"{i:2d}. {agent}")
    
    if len(agents_list) > 15:
        print(f"   ... et {len(agents_list)-15} autres")
    
    print("\n" + "─" * 40)
    
    agent_input = input("\nNom ou numéro de l'agent: ")
    
    try:
        if agent_input.isdigit():
            idx = int(agent_input) - 1
            if 0 <= idx < len(agents_list):
                agent_name = agents_list[idx]
            else:
                print("❌ Numéro invalide!")
                input("\n↵ Appuyez sur Entrée pour continuer...")
                return
        else:
            agent_name = agent_input
        
        if not agent_name.endswith(".py"):
            agent_name += ".py"
        
        if os.path.exists(f"/root/{agent_name}"):
            print(f"\n🚀 Lancement de: {agent_name}")
            print("   Mode: [1] Avant-plan  [2] Arrière-plan  [3] Test")
            
            mode = input("   Choix (1-3): ")
            
            if mode == "1":
                print(f"\n⏳ Exécution en cours...")
                os.system(f"python3 /root/{agent_name}")
            elif mode == "2":
                log_file = f"/tmp/{agent_name.replace('.py', '')}_{os.getpid()}.log"
                os.system(f"nohup python3 /root/{agent_name} > {log_file} 2>&1 &")
                print(f"\n✅ Agent lancé en arrière-plan")
                print(f"📄 Log: {log_file}")
            elif mode == "3":
                print(f"\n🧪 Test rapide de {agent_name}")
                os.system(f"python3 /root/{agent_name} --help 2>/dev/null || echo 'Pas d\'aide disponible'")
            else:
                print("❌ Mode invalide!")
        else:
            print(f"❌ Agent '{agent_name}' non trouvé!")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    input("\n↵ Appuyez sur Entrée pour continuer...")

def main_menu():
    while True:
        clear_screen()
        print("╔══════════════════════════════════════╗")
        print("║     SYSTÈME D'AGENTS IA v2.0        ║")
        print("║        " + str(len([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])).rjust(2) + " AGENTS ACTIFS              ║")
        print("╚══════════════════════════════════════╝")
        
        print("\n" + " " * 10 + "📋 MENU PRINCIPAL")
        print(" " * 8 + "═" * 24)
        
        print("\n   1. 📊 Tableau de bord")
        print("   2. 📜 Liste des agents")
        print("   3. 🚀 Lancer un agent")
        print("   4. ⚙️  Outils système")
        print("   5. ❌ Quitter")
        
        print("\n" + "─" * 40)
        
        choix = input("   Votre choix (1-5): ")
        
        if choix == "1":
            show_stats()
        elif choix == "2":
            list_agents()
        elif choix == "3":
            launch_agent()
        elif choix == "4":
            clear_screen()
            print("╔══════════════════════════════════════╗")
            print("║          OUTILS SYSTÈME            ║")
            print("╚══════════════════════════════════════╝")
            
            print("\n   1. 📁 Lister tous les fichiers Python")
            print("   2. 🔍 Voir les processus en cours")
            print("   3. 💾 Vérifier l'espace disque")
            print("   4. 📶 Tester la connexion")
            print("   5. ↩️  Retour")
            
            outil = input("\n   Choix (1-5): ")
            
            if outil == "1":
                clear_screen()
                print("Fichiers Python dans /root:\n")
                os.system("ls /root/*.py | wc -l && echo '' && ls /root/*.py | head -20")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            elif outil == "2":
                clear_screen()
                print("Processus Python en cours:\n")
                os.system("ps aux | grep python | grep -v grep | head -20")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            elif outil == "3":
                clear_screen()
                print("Espace disque:\n")
                os.system("df -h")
                input("\n↵ Appuyez sur Entrée pour continuer...")
            elif outil == "4":
                clear_screen()
                print("Test de connexion:\n")
                os.system("ping -c 2 google.com 2>/dev/null || echo 'Ping non disponible'")
                input("\n↵ Appuyez sur Entrée pour continuer...")
        
        elif choix == "5":
            clear_screen()
            print("\n" + "=" * 40)
            print("   Merci d'avoir utilisé le système!")
            print("   👋 Au revoir!")
            print("=" * 40 + "\n")
            sys.exit(0)
        
        else:
            print("\n❌ Choix invalide!")
            input("↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interruption par l'utilisateur")
        sys.exit(0)
EOF

chmod +x /root/menu_final.py
python3 /root/menu_final.py
