cat > /root/menu_simple.py << 'EOF'
#!/usr/bin/env python3
import os
import sys

while True:
    print("\n=== MENU SIMPLE ===")
    print("1. Lister agents")
    print("2. Tableau de bord")
    print("3. Quitter")
    
    choix = input("Choix: ")
    
    if choix == "1":
        agents = os.listdir("/root")
        agents = [a for a in agents if a.startswith("agent_") and a.endswith(".py")]
        for a in agents:
            print(f"  - {a}")
        print(f"Total: {len(agents)} agents")
    
    elif choix == "2":
        print(f"\nPython: {len([f for f in os.listdir('/root') if f.endswith('.py')])}")
        print(f"Agents: {len([f for f in os.listdir('/root') if f.startswith('agent_')])}")
        print(f"Menus: {len([f for f in os.listdir('/root') if 'menu' in f.lower() and f.endswith('.py')])}")
        print(f"Interfaces: {len([f for f in os.listdir('/root') if 'interface' in f.lower() and f.endswith('.py')])}")
    
    elif choix == "3":
        print("Au revoir!")
        sys.exit()
EOF
