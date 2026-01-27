cat > menu.py << 'EOF'
#!/usr/bin/env python3
# Menu simple pour votre système IA

import os
import subprocess

print("=" * 50)
print("🤖 SYSTÈME IA - MENU PRINCIPAL")
print("=" * 50)

# Afficher les statistiques
print("\n📊 VOTRE SYSTÈME CONTIENT:")
for dossier, nom in [("AGENTS", "Agents IA"), ("APIS", "APIs"), ("SCRIPTS", "Scripts"), ("WEB", "Sites Web")]:
    if os.path.exists(dossier):
        nb = len([f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))])
        print(f"  {nom}: {nb} fichiers")

while True:
    print("\n" + "-" * 40)
    print("MENU:")
    print("1. 🤖 Voir mes agents IA")
    print("2. 🚀 Lancer un agent")
    print("3. 🌐 Voir mes APIs")
    print("4. 🛠️ Voir mes scripts")
    print("5. 🌍 Voir mes sites web")
    print("6. ❌ Quitter")
    print("-" * 40)
    
    choix = input("\nVotre choix (1-6): ")
    
    if choix == "1":
        print("\n🤖 VOS AGENTS IA:")
        print("-" * 30)
        if os.path.exists("AGENTS"):
            agents = [f for f in os.listdir("AGENTS") if f.endswith(".py")]
            for i, agent in enumerate(agents, 1):
                print(f"{i}. {agent}")
            if not agents:
                print("Aucun agent trouvé")
        else:
            print("Dossier AGENTS/ non trouvé")
    
    elif choix == "2":
        if os.path.exists("AGENTS"):
            agents = [f for f in os.listdir("AGENTS") if f.endswith(".py")]
            if agents:
                print("\nQuel agent voulez-vous lancer ?")
                for i, agent in enumerate(agents, 1):
                    print(f"{i}. {agent}")
                
                try:
                    num = int(input("\nNuméro de l'agent: ")) - 1
                    if 0 <= num < len(agents):
                        print(f"\n🚀 Lancement de {agents[num]}...")
                        subprocess.run(["python3", f"AGENTS/{agents[num]}"])
                    else:
                        print("❌ Numéro invalide")
                except:
                    print("❌ Entrée invalide")
            else:
                print("❌ Aucun agent disponible")
        else:
            print("❌ Dossier AGENTS/ non trouvé")
    
    elif choix == "3":
        print("\n🌐 VOS APIs:")
        print("-" * 30)
        if os.path.exists("APIS"):
            for f in os.listdir("APIS"):
                print(f"📄 {f}")
        else:
            print("Dossier APIS/ non trouvé")
    
    elif choix == "4":
        print("\n🛠️ VOS SCRIPTS:")
        print("-" * 30)
        if os.path.exists("SCRIPTS"):
            for f in os.listdir("SCRIPTS"):
                print(f"📄 {f}")
        else:
            print("Dossier SCRIPTS/ non trouvé")
    
    elif choix == "5":
        print("\n🌍 VOS SITES WEB:")
        print("-" * 30)
        if os.path.exists("WEB"):
            for f in os.listdir("WEB"):
                print(f"📄 {f}")
        else:
            print("Dossier WEB/ non trouvé")
    
    elif choix == "6":
        print("\n👋 Au revoir !")
        break
    
    else:
        print("❌ Choix invalide. Veuillez choisir entre 1 et 6.")
    
    input("\n↵ Appuyez sur Entrée pour continuer...")
EOF
