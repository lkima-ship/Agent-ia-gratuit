cat > menu.py << 'EOF'
#!/usr/bin/env python3
import os
import subprocess

def afficher_statistiques():
    print("\n📊 STATISTIQUES DU SYSTÈME:")
    print("-" * 40)
    
    dossiers = {
        "AGENTS": "🤖 Agents IA",
        "APIS": "🌐 APIs & Serveurs", 
        "SCRIPTS": "🛠️ Scripts",
        "WEB": "🌍 Sites Web",
        "MENUS": "📋 Menus"
    }
    
    for dossier, nom in dossiers.items():
        if os.path.exists(dossier):
            fichiers = [f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))]
            print(f"{nom}: {len(fichiers)} fichiers")
        else:
            print(f"{nom}: 0 fichiers (dossier manquant)")

def lister_agents():
    print("\n🤖 LISTE DES AGENTS IA:")
    print("-" * 40)
    
    if os.path.exists("AGENTS"):
        agents = [f for f in os.listdir("AGENTS") if f.endswith(".py")]
        if agents:
            for i, agent in enumerate(agents, 1):
                print(f"{i}. {agent}")
            return agents
        else:
            print("Aucun agent trouvé")
    else:
        print("Dossier AGENTS/ non trouvé")
    
    return []

def lancer_agent(agent_name):
    chemin = f"AGENTS/{agent_name}"
    if os.path.exists(chemin):
        print(f"\n🚀 Lancement de {agent_name}...")
        try:
            subprocess.run(["python3", chemin])
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print(f"❌ Fichier non trouvé: {chemin}")

def afficher_menu_principal():
    print("\n" + "=" * 60)
    print("🤖 SYSTÈME IA - MENU PRINCIPAL")
    print("=" * 60)
    print("1. 📊 Voir les statistiques")
    print("2. 🤖 Lister tous les agents")
    print("3. 🚀 Lancer un agent")
    print("4. 🌐 Voir les APIs disponibles")
    print("5. 🛠️ Voir les scripts disponibles")
    print("6. 🔄 Réorganiser les fichiers")
    print("7. ❌ Quitter")
    print("=" * 60)

def main():
    print("✅ Système organisé avec succès!")
    
    while True:
        afficher_menu_principal()
        choix = input("\n👉 Votre choix (1-7): ").strip()
        
        if choix == "1":
            afficher_statistiques()
            
        elif choix == "2":
            agents = lister_agents()
            if agents:
                print(f"\nTotal: {len(agents)} agents disponibles")
                
        elif choix == "3":
            agents = lister_agents()
            if agents:
                try:
                    choix_agent = int(input("\n👉 Numéro de l'agent à lancer: ")) - 1
                    if 0 <= choix_agent < len(agents):
                        lancer_agent(agents[choix_agent])
                    else:
                        print("❌ Numéro invalide")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide")
                    
        elif choix == "4":
            print("\n🌐 APIs DISPONIBLES:")
            print("-" * 40)
            if os.path.exists("APIS"):
                for f in os.listdir("APIS"):
                    print(f"📄 {f}")
            else:
                print("Dossier APIS/ non trouvé")
                
        elif choix == "5":
            print("\n🛠️ SCRIPTS DISPONIBLES:")
            print("-" * 40)
            if os.path.exists("SCRIPTS"):
                for f in os.listdir("SCRIPTS"):
                    print(f"📄 {f}")
            else:
                print("Dossier SCRIPTS/ non trouvé")
                
        elif choix == "6":
            print("\n🔄 Réorganisation des fichiers...")
            # Vous pouvez réexécuter les commandes d'organisation ici
            print("Cette fonctionnalité sera implémentée ultérieurement")
            
        elif choix == "7":
            print("\n👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide!")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF
