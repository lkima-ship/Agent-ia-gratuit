cat > /root/menu.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
import time

while True:
    print("\n" + "="*40)
    print("       MENU PRINCIPAL")
    print("="*40)
    print("1. 📋 Lister tous les agents")
    print("2. 📊 Afficher les statistiques")
    print("3. 🚀 Lancer un agent")
    print("4. ⚙️  Gérer les processus")
    print("5. 🏠 Accéder au système organisé")
    print("6. ❌ Quitter")
    print("="*40)
    
    choix = input("Votre choix (1-6): ")
    
    if choix == "1":
        print("\n" + "-"*40)
        print("LISTE DES AGENTS:")
        print("-"*40)
        agents = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
        for i, agent in enumerate(agents, 1):
            print(f"{i:3d}. {agent}")
        print(f"\nTotal: {len(agents)} agents")
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "2":
        print("\n" + "-"*40)
        print("STATISTIQUES:")
        print("-"*40)
        print(f"Fichiers Python: {len([f for f in os.listdir('/root') if f.endswith('.py')])}")
        print(f"Agents (agent_*): {len([f for f in os.listdir('/root') if f.startswith('agent_')])}")
        print(f"Menus: {len([f for f in os.listdir('/root') if 'menu' in f.lower() and f.endswith('.py')])}")
        print(f"Interfaces: {len([f for f in os.listdir('/root') if 'interface' in f.lower() and f.endswith('.py')])}")
        print(f"Dashboards: {len([f for f in os.listdir('/root') if 'dashboard' in f.lower() and f.endswith('.py')])}")
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "3":
        agents = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
        print("\n" + "-"*40)
        print("LANCEUR D'AGENT:")
        print("-"*40)
        print("Top 10 agents:")
        for i, agent in enumerate(agents[:10], 1):
            print(f"{i:2d}. {agent}")
        if len(agents) > 10:
            print(f"   ... et {len(agents)-10} autres")
        
        agent_choix = input("\nNom ou numéro de l'agent: ")
        
        try:
            if agent_choix.isdigit():
                idx = int(agent_choix) - 1
                if 0 <= idx < len(agents):
                    agent_choix = agents[idx]
            
            if os.path.exists(f"/root/{agent_choix}"):
                print(f"\nLancement de '{agent_choix}'...")
                # Créer un fichier log pour cet agent
                log_file = f"/tmp/{agent_choix}.log"
                os.system(f"python3 /root/{agent_choix} > {log_file} 2>&1 &")
                print(f"✅ Agent lancé en arrière-plan")
                print(f"📝 Logs: {log_file}")
            else:
                print("❌ Agent non trouvé")
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "4":
        print("\n" + "-"*40)
        print("GESTION DES PROCESSUS:")
        print("-"*40)
        print("1. Voir tous les processus")
        print("2. Arrêter un agent")
        print("3. Arrêter tous les agents")
        print("-"*40)
        
        sous_choix = input("Choix (1-3): ")
        
        if sous_choix == "1":
            print("\nProcessus agents en cours:")
            os.system("ps aux | grep 'python3.*agent_' | grep -v grep")
        elif sous_choix == "2":
            pid = input("Entrez le PID à arrêter: ")
            os.system(f"kill {pid}")
            print(f"✅ Processus {pid} arrêté")
        elif sous_choix == "3":
            os.system("pkill -f 'python3.*agent_'")
            print("✅ Tous les agents arrêtés")
        else:
            print("❌ Choix invalide")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "5":
        print("\n" + "-"*40)
        print("SYSTÈME ORGANISÉ:")
        print("-"*40)
        
        # Vérifier si le système organisé existe
        if os.path.exists("/root/ia_system"):
            print("Système organisé trouvé!")
            print("1. Accéder au dossier")
            print("2. Lancer le système")
            print("3. Voir la structure")
            
            sous_choix = input("Choix (1-3): ")
            
            if sous_choix == "1":
                os.chdir("/root/ia_system")
                print("✅ Changé vers /root/ia_system")
                print(f"Répertoire actuel: {os.getcwd()}")
            elif sous_choix == "2":
                if os.path.exists("/root/ia_system/menu.py"):
                    os.system("cd /root/ia_system && python3 menu.py")
                else:
                    print("❌ menu.py non trouvé dans ia_system")
            elif sous_choix == "3":
                os.system("ls -la /root/ia_system/")
            else:
                print("❌ Choix invalide")
        else:
            print("❌ Système organisé non trouvé")
            print("   Créez-le avec: mkdir /root/ia_system")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "6":
        print("\n" + "="*40)
        print("Au revoir ! 👋")
        print("="*40)
        sys.exit(0)
    
    else:
        print("❌ Choix invalide !")
        time.sleep(1)
EOF
