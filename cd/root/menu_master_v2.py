# Mettre à jour menu_master.py pour inclure les nouvelles versions
cat > menu_master_v2.py << 'EOF'
#!/usr/bin/env python3
"""
MASTER MENU V2 - Tous vos agents IA améliorés
"""
import os
import subprocess
import sys

print("="*60)
print("           🚀 MASTER MENU V2 - AGENTS IA PRO")
print("="*60)

AGENTS = {
    "1": {"fichier": "agent_ia_ml.py", "nom": "🧠 Agent IA ML", "desc": "Machine Learning"},
    "2": {"fichier": "agent_analyse_donnees.py", "nom": "📊 Analyse Données V2", "desc": "Analyse CSV/JSON avancée"},
    "3": {"fichier": "agent_web_avance.py", "nom": "🌐 Agent Web Avancé", "desc": "Scraping et API"},
    "4": {"fichier": "agent_surveillance.py", "nom": "🔧 Surveillance Système", "desc": "Monitoring CPU/RAM"},
    "5": {"fichier": "agent_ia_gratuit.py", "nom": "🤖 Agent IA Gratuit V3", "desc": "Assistant IA complet"},
    "6": {"fichier": "agent_ia_pro.py", "nom": "⚡ Agent IA Pro", "desc": "Version professionnelle"},
    "7": {"fichier": "agent_ia_complet.py", "nom": "🎯 Agent IA Complet", "desc": "Toutes fonctionnalités"},
    "8": {"fichier": "hub_agents.py", "nom": "📋 Hub Agents", "desc": "Gestion des agents"},
    "9": {"fichier": "agent_web_simple.py", "nom": "🌍 Agent Web Simple", "desc": "Test URL basique"},
    "10": {"fichier": "menu_commandes.py", "nom": "⚙️ Menu Commandes", "desc": "Commandes rapides"},
    "11": {"fichier": "ia_dashboard.py", "nom": "📈 Dashboard IA", "desc": "Vue d'ensemble"},
    "12": {"fichier": "start_ia.sh", "nom": "🚀 Script Démarrage", "desc": "Lancement automatique"},
    "0": {"fichier": None, "nom": "🚪 Quitter", "desc": "Fermer l'application"}
}

def afficher_menu():
    print("\n📋 AGENTS DISPONIBLES :")
    print("-"*60)
    
    agents_ok = 0
    for key, agent in AGENTS.items():
        if key == "0":
            print(f"{key}. {agent['nom']}")
        else:
            existe = os.path.exists(agent['fichier'])
            statut = "✅" if existe else "❌"
            print(f"{key}. {statut} {agent['nom']} - {agent['desc']}")
            if existe:
                agents_ok += 1
    
    print(f"\n📊 {agents_ok}/{len(AGENTS)-1} agents disponibles")
    print("="*60)

def main():
    while True:
        afficher_menu()
        
        choix = input("👉 Choisissez un agent (0-12) : ")
        
        if choix in AGENTS:
            agent = AGENTS[choix]
            
            if choix == "0":
                print("\n👋 Au revoir ! Développez vos idées avec IA !")
                break
            
            fichier = agent['fichier']
            
            if not os.path.exists(fichier):
                print(f"\n❌ Fichier {fichier} non trouvé !")
                print(f"Description : {agent['desc']}")
                print("\nVoulez-vous :")
                print("1. Créer une version basique")
                print("2. Ignorer et continuer")
                
                sous_choix = input("Votre choix : ")
                
                if sous_choix == "1":
                    print(f"\n📝 Création de {fichier}...")
                    with open(fichier, 'w') as f:
                        f.write(f'#!/usr/bin/env python3\nprint("{agent["nom"]}")\nprint("{agent["desc"]}")\n')
                    os.chmod(fichier, 0o755)
                    print(f"✅ {fichier} créé")
                else:
                    print("⏭️  Passé au suivant")
                    continue
            
            if os.path.exists(fichier):
                print(f"\n🚀 Lancement de {agent['nom']}...")
                print(f"📋 {agent['desc']}")
                print("="*40)
                try:
                    # Vérifier si c'est un script shell
                    if fichier.endswith('.sh'):
                        subprocess.run(["sh", fichier])
                    else:
                        subprocess.run([sys.executable, fichier])
                except KeyboardInterrupt:
                    print("\n⏹️  Interruption - Retour au menu")
                except Exception as e:
                    print(f"❌ Erreur : {e}")
            else:
                print(f"❌ Impossible de lancer {fichier}")
            
            input("\n↵ Appuyez sur Entrée pour continuer...")
        else:
            print("❌ Choix invalide !")
            input("↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF

# Remplacer l'ancien menu
mv menu_master.py menu_master_old.py
mv menu_master_v2.py menu_master.py
chmod +x menu_master.py

# Tester le nouveau menu
python3 menu_master.py
