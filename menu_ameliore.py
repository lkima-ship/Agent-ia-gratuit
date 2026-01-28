cat > menu_ameliore.py << 'EOF'
#!/usr/bin/env python3
# Menu amélioré pour votre système IA

import os
import subprocess
import sys

def afficher_en_tete():
    print("╔══════════════════════════════════════════════════════════╗")
    print("║                 🤖 SYSTÈME IA COMPLET                    ║")
    print("╚══════════════════════════════════════════════════════════╝")

def afficher_stats():
    print("\n📊 STATISTIQUES:")
    print("─" * 40)
    
    stats = {
        "🤖 AGENTS IA": "AGENTS",
        "🌐 APIs": "APIS", 
        "🛠️ SCRIPTS": "SCRIPTS",
        "🌍 SITES WEB": "WEB"
    }
    
    for nom, dossier in stats.items():
        if os.path.isdir(dossier):
            nb = len([f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))])
            print(f"  {nom}: {nb} fichiers")
        else:
            print(f"  {nom}: dossier manquant")

def lister_agents():
    print("\n🤖 AGENTS DISPONIBLES:")
    print("─" * 40)
    
    if not os.path.exists("AGENTS"):
        print("Dossier AGENTS/ non trouvé")
        return []
    
    agents = []
    for f in os.listdir("AGENTS"):
        if f.endswith(".py") and os.path.isfile(os.path.join("AGENTS", f)):
            agents.append(f)
    
    if not agents:
        print("Aucun agent trouvé")
        return []
    
    for i, agent in enumerate(agents, 1):
        print(f"{i}. {agent}")
    
    return agents

def lancer_agent(agent_name):
    chemin = f"AGENTS/{agent_name}"
    if os.path.exists(chemin):
        print(f"\n🚀 Lancement de {agent_name}...")
        print("─" * 40)
        try:
            result = subprocess.run(
                [sys.executable, chemin],
                capture_output=True,
                text=True
            )
            if result.stdout:
                print("📤 Sortie:")
                print(result.stdout)
            if result.stderr:
                print("⚠️  Erreurs:")
                print(result.stderr)
        except Exception as e:
            print(f"❌ Erreur: {e}")
    else:
        print(f"❌ Fichier non trouvé: {chemin}")

def main():
    afficher_en_tete()
    afficher_stats()
    
    while True:
        print("\n" + "═" * 60)
        print("MENU PRINCIPAL:")
        print("═" * 60)
        print("1. 📋 Lister tous les agents")
        print("2. 🚀 Lancer un agent spécifique")
        print("3. 🌐 Voir les APIs disponibles")
        print("4. 🛠️  Voir les scripts")
        print("5. 🌍 Voir les sites web")
        print("6. 🧪 Tester le système")
        print("7. 🆘 Aide")
        print("0. ❌ Quitter")
        print("═" * 60)
        
        choix = input("\n👉 Sélectionnez une option (0-7): ").strip()
        
        if choix == "1":
            agents = lister_agents()
            if agents:
                print(f"\n✅ Total: {len(agents)} agents disponibles")
        
        elif choix == "2":
            agents = lister_agents()
            if agents:
                try:
                    num = int(input(f"\n👉 Numéro de l'agent (1-{len(agents)}): "))
                    if 1 <= num <= len(agents):
                        lancer_agent(agents[num-1])
                    else:
                        print(f"❌ Veuillez entrer un nombre entre 1 et {len(agents)}")
                except ValueError:
                    print("❌ Veuillez entrer un nombre valide")
        
        elif choix == "3":
            print("\n🌐 APIs DISPONIBLES:")
            print("─" * 40)
            if os.path.exists("APIS"):
                for f in os.listdir("APIS"):
                    if f.endswith('.py'):
                        print(f"📄 {f}")
            else:
                print("Dossier APIS/ manquant")
        
        elif choix == "4":
            print("\n🛠️ SCRIPTS DISPONIBLES:")
            print("─" * 40)
            if os.path.exists("SCRIPTS"):
                # Afficher seulement les 10 premiers scripts
                scripts = [f for f in os.listdir("SCRIPTS") if f.endswith('.sh')]
                for script in scripts[:10]:
                    print(f"📄 {script}")
                if len(scripts) > 10:
                    print(f"... et {len(scripts) - 10} autres")
            else:
                print("Dossier SCRIPTS/ manquant")
        
        elif choix == "5":
            print("\n🌍 SITES WEB:")
            print("─" * 40)
            if os.path.exists("WEB"):
                for f in os.listdir("WEB"):
                    if f.endswith(('.html', '.htm')):
                        print(f"📄 {f}")
            else:
                print("Dossier WEB/ manquant")
        
        elif choix == "6":
            print("\n🧪 TEST DU SYSTÈME:")
            print("─" * 40)
            print("1. Vérification Python...")
            try:
                subprocess.run([sys.executable, "--version"], check=True)
                print("   ✅ Python fonctionne")
            except:
                print("   ❌ Problème avec Python")
            
            print("\n2. Vérification des dossiers...")
            for dossier in ["AGENTS", "APIS", "SCRIPTS", "WEB"]:
                if os.path.isdir(dossier):
                    nb = len([f for f in os.listdir(dossier) if os.path.isfile(os.path.join(dossier, f))])
                    print(f"   ✅ {dossier}: {nb} fichiers")
                else:
                    print(f"   ❌ {dossier}: manquant")
        
        elif choix == "7":
            print("\n🆘 AIDE:")
            print("─" * 40)
            print("Commandes utiles:")
            print("  • python3 menu_ameliore.py  - Ce menu")
            print("  • python3 AGENTS/[nom].py   - Lancer un agent")
            print("  • python3 APIS/[nom].py     - Lancer une API")
            print("  • ls AGENTS/               - Voir les agents")
            print("  • ls APIS/                 - Voir les APIs")
            print("\nExemples:")
            print("  • python3 AGENTS/index_agents.py")
            print("  • python3 AGENTS/suite_agents_ia.py")
            print("  • python3 APIS/simple_api.py")
        
        elif choix == "0":
            print("\n👋 Au revoir ! Merci d'avoir utilisé le système IA.")
            break
        
        else:
            print("❌ Option invalide. Veuillez choisir entre 0 et 7.")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption par l'utilisateur.")
        sys.exit(0)
EOF
