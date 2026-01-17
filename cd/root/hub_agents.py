cd /root

# Recréer hub_agents.py avec la bonne indentation
cat > hub_agents.py << 'EOF'
#!/usr/bin/env python3
"""
HUB DES AGENTS - Version corrigée
"""
import os
import subprocess
import sys

def afficher_menu():
    os.system('clear')
    print("="*60)
    print("           🎮 HUB DES AGENTS IA")
    print("="*60)
    
    AGENTS = [
        ("agent_web_simple.py", "🌐 Agent Web Simple"),
        ("moniteur_reseau.py", "📡 Moniteur Réseau"),
        ("dashboard_web_agent.py", "🖥️ Dashboard Web"),
        ("agent_simple_ia.py", "🤖 Agent IA Simple"),
        ("menu_commandes.py", "⚙️ Menu Commandes"),
        ("menu_final.py", "📊 Menu Final")
    ]
    
    agents_disponibles = []
    for fichier, nom in AGENTS:
        if os.path.exists(fichier):
            agents_disponibles.append((fichier, nom))
    
    if not agents_disponibles:
        print("❌ Aucun agent trouvé !")
        return []
    
    print("📋 Agents disponibles :")
    for i, (fichier, nom) in enumerate(agents_disponibles, 1):
        print(f"{i}. {nom}")
    
    print(f"\n{len(agents_disponibles)}/{len(AGENTS)} agents trouvés")
    print("-"*60)
    
    return agents_disponibles

def main():
    while True:
        agents = afficher_menu()
        
        if not agents:
            print("Appuyez sur Entrée pour quitter...")
            input()
            break
        
        choix = input("👉 Choisissez un agent (numéro) ou '0' pour quitter : ")
        
        if choix == "0":
            print("👋 Au revoir !")
            break
        
        try:
            choix_int = int(choix)
            if 1 <= choix_int <= len(agents):
                fichier, nom = agents[choix_int - 1]
                print(f"\n🚀 Lancement de {nom}...")
                print("-"*40)
                subprocess.run([sys.executable, fichier])
                input("\n↵ Appuyez sur Entrée pour continuer...")
            else:
                print("❌ Choix invalide. Veuillez choisir entre 1 et", len(agents))
                input("\n↵ Appuyez sur Entrée pour continuer...")
        except ValueError:
            print("❌ Veuillez entrer un nombre valide")
            input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF

# Tester la version corrigée
python3 hub_agents.py
