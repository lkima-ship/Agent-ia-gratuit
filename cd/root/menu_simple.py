cat > /root/menu_clean.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

while True:
    print("\n" + "="*30)
    print("MENU AGENTS IA")
    print("="*30)
    print("1. Lister les agents")
    print("2. Statistiques")
    print("3. Quitter")
    print("="*30)
    
    choix = input("Votre choix: ")
    
    if choix == "1":
        print("\nListe des agents:")
        agents = [f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")]
        for i, agent in enumerate(agents, 1):
            print(f"{i:2d}. {agent}")
        print(f"\nTotal: {len(agents)} agents")
        input("\nAppuyez sur Entrée...")
    
    elif choix == "2":
        print("\nStatistiques:")
        print(f"Fichiers Python: {len([f for f in os.listdir('/root') if f.endswith('.py')])}")
        print(f"Agents: {len([f for f in os.listdir('/root') if f.startswith('agent_')])}")
        print(f"Menus: {len([f for f in os.listdir('/root') if 'menu' in f.lower() and f.endswith('.py')])}")
        input("\nAppuyez sur Entrée...")
    
    elif choix == "3":
        print("\nAu revoir!")
        sys.exit()
    
    else:
        print("Choix invalide!")
EOF

chmod +x /root/menu_clean.py
python3 /root/menu_clean.py
