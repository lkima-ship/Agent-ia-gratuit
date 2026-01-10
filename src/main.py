cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Agent IA Gratuit - Point d'entrée principal
"""

def main():
    print("🤖 Agent IA Gratuit")
    print("===================")
    print("Options disponibles:")
    print("1. Démarrer le serveur web")
    print("2. Afficher la structure")
    print("3. Quitter")
    
    try:
        choice = input("\nVotre choix (1-3): ")
        
        if choice == "1":
            print("\n🚀 Démarrage du serveur web...")
            try:
                # Importer et exécuter le serveur
                from src.simple_server import run_server
                run_server()
            except ImportError:
                print("❌ Erreur: simple_server.py non trouvé")
                print("Exécutez: python3 src/simple_server.py directement")
                
        elif choice == "2":
            print("\n📁 Structure du projet:")
            import os
            for root, dirs, files in os.walk("."):
                level = root.replace(".", "").count(os.sep)
                indent = " " * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = " " * 2 * (level + 1)
                for file in files:
                    if file.endswith(".py"):
                        print(f"{subindent}{file}")
                        
        elif choice == "3":
            print("\nAu revoir! 👋")
            return
            
        else:
            print("\n⚠️ Choix invalide")
            
    except KeyboardInterrupt:
        print("\n\nInterrompu par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main()
EOF
