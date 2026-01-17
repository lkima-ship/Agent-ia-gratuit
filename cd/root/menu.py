cat > /root/menu.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

while True:
    print("\n" + "="*40)
    print("       MENU PRINCIPAL")
    print("="*40)
    print("1. 📋 Lister tous les agents")
    print("2. 📊 Afficher les statistiques")
    print("3. 🚀 Lancer un agent")
    print("4. ❌ Quitter")
    print("="*40)
    
    choix = input("Votre choix (1-4): ")
    
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
                os.system(f"python3 /root/{agent_choix} &")
                print(f"✅ Agent lancé en arrière-plan")
            else:
                print("❌ Agent non trouvé")
        except:
            print("❌ Erreur de saisie")
        
        input("\nAppuyez sur Entrée pour continuer...")
    
    elif choix == "4":
        print("\n" + "="*40)
        print("Au revoir ! 👋")
        print("="*40)
        sys.exit(0)
    
    else:
        print("❌ Choix invalide !")
        input("Appuyez sur Entrée pour continuer...")
EOF
