cat > menu.py << 'EOF'
#!/usr/bin/env python3
import os
import subprocess

while True:
    print("\n" + "="*50)
    print("🤖 VOTRE SYSTÈME IA")
    print("="*50)
    print("1. Voir les AGENTS")
    print("2. Voir les APIs")
    print("3. Voir les scripts")
    print("4. Lancer un agent")
    print("5. Quitter")
    print("="*50)
    
    choix = input("\nVotre choix: ")
    
    if choix == "1":
        print("\n📁 AGENTS:")
        if os.path.exists("AGENTS"):
            for f in os.listdir("AGENTS"):
                print(f"  - {f}")
        else:
            print("Dossier AGENTS/ non trouvé")
    
    elif choix == "2":
        print("\n🌐 APIs:")
        if os.path.exists("APIS"):
            for f in os.listdir("APIS"):
                print(f"  - {f}")
    
    elif choix == "3":
        print("\n🛠️ SCRIPTS:")
        if os.path.exists("SCRIPTS"):
            for f in os.listdir("SCRIPTS"):
                print(f"  - {f}")
    
    elif choix == "4":
        if os.path.exists("AGENTS"):
            agents = [f for f in os.listdir("AGENTS") if f.endswith(".py")]
            if agents:
                print("\nChoisissez un agent:")
                for i, a in enumerate(agents, 1):
                    print(f"{i}. {a}")
                
                try:
                    num = int(input("Numéro: ")) - 1
                    if 0 <= num < len(agents):
                        print(f"\n🚀 Lancement: {agents[num]}")
                        os.system(f"python3 AGENTS/{agents[num]}")
                except:
                    print("❌ Choix invalide")
    
    elif choix == "5":
        print("\n👋 Au revoir!")
        break
    
    else:
        print("❌ Choix invalide")
    
    input("\nAppuyez sur Entrée pour continuer...")
EOF
