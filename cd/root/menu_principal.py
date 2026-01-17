cat > /root/menu_principal.py << 'EOF'
#!/usr/bin/env python3
"""
Menu Principal - Système d'Agents IA - Version Améliorée
"""

import os
import sys

def afficher_stats():
    """Affiche les statistiques du système"""
    agents = [f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")]
    tous_python = [f for f in os.listdir("/root") if f.endswith(".py")]
    menus = [f for f in os.listdir("/root") if "menu" in f.lower() and f.endswith(".py")]
    
    print("\n" + "="*50)
    print("📊 TABLEAU DE BORD")
    print("="*50)
    print(f"\n📁 Fichiers Python: {len(tous_python)}")
    print(f"🚀 Agents IA: {len(agents)}")
    print(f"📋 Menus: {len(menus)}")
    print(f"🖥️  Interfaces: {len([f for f in tous_python if 'interface' in f.lower()])}")
    
    print("\n🔍 AGENTS PRINCIPAUX:")
    for agent in ["hub_agents.py", "agent_web_avance.py", "menu_principal.py"]:
        if os.path.exists(f"/root/{agent}"):
            print(f"  ✅ {agent}")
        else:
            print(f"  ❌ {agent} (manquant)")
    
    input("\nAppuyez sur Entrée pour continuer...")

def afficher_menu():
    """Affiche le menu principal"""
    print("\n" + "="*50)
    print("🤖 SYSTÈME D'AGENTS IA")
    print("="*50)
    
    agents = [f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")]
    
    print(f"\n📋 {len(agents)} agents disponibles")
    
    print("\nOptions:")
    print("  1. 📜 Lister tous les agents")
    print("  2. 🚀 Lancer un agent")
    print("  3. 📊 Tableau de bord")
    print("  4. 🛠️  Outils système")
    print("  5. ❌ Quitter")
    
    return input("\nVotre choix: ")

def main():
    while True:
        choix = afficher_menu()
        
        if choix == "1":
            agents = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
            print("\n" + "="*50)
            print("📜 LISTE COMPLÈTE DES AGENTS")
            print("="*50)
            for i, agent in enumerate(agents, 1):
                print(f"  {i:2d}. {agent}")
            print(f"\nTotal: {len(agents)} agents")
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "2":
            agents = sorted([f for f in os.listdir("/root") if f.startswith("agent_") and f.endswith(".py")])
            print("\nAgents disponibles:")
            for i, agent in enumerate(agents[:10], 1):
                print(f"  {i}. {agent}")
            if len(agents) > 10:
                print(f"  ... et {len(agents)-10} autres")
            
            try:
                choix_agent = input("\nNuméro ou nom de l'agent: ")
                if choix_agent.isdigit():
                    index = int(choix_agent) - 1
                    if 0 <= index < len(agents):
                        choix_agent = agents[index]
                
                if os.path.exists(f"/root/{choix_agent}"):
                    print(f"\nLancement de {choix_agent}...")
                    os.system(f"python3 /root/{choix_agent} &")
                    print("✅ Agent lancé en arrière-plan")
                else:
                    print("❌ Agent non trouvé")
            except:
                print("❌ Choix invalide")
            
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "3":
            afficher_stats()
            
        elif choix == "4":
            print("\n" + "="*50)
            print("🛠️  OUTILS SYSTÈME")
            print("="*50)
            print("\n1. Vérifier l'espace disque")
            print("2. Voir les processus")
            print("3. Retour")
            
            sous_choix = input("\nChoix: ")
            if sous_choix == "1":
                os.system("df -h /")
            elif sous_choix == "2":
                os.system("ps aux | grep python | head -20")
            
            input("\nAppuyez sur Entrée pour continuer...")
            
        elif choix == "5":
            print("\n👋 Au revoir !")
            sys.exit(0)
            
        else:
            print("❌ Choix invalide")
            input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF
