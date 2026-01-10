cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Point d'entrée principal de l'Agent IA Gratuit
"""

import sys
import subprocess

def main():
    print("🤖 Agent IA Gratuit")
    print("==================")
    print("Options disponibles:")
    print("1. Lancer le serveur web")
    print("2. Tester l'API")
    print("3. Quitter")
    
    try:
        choice = input("\nChoisissez une option (1-3): ").strip()
        
        if choice == "1":
            print("\n" + "="*40)
            print("Lancement du serveur web...")
            print("="*40)
            # Importer et exécuter le serveur directement
            from src.simple_server import run_server
            run_server()
            
        elif choice == "2":
            print("\nTest de l'API...")
            import requests
            try:
                response = requests.get("http://localhost:8000", timeout=2)
                print(f"✅ Serveur répond: {response.status_code}")
                print(f"📦 Contenu: {response.json()}")
            except Exception as e:
                print(f"❌ Erreur: {e}")
                print("Le serveur ne semble pas fonctionner.")
                launch = input("Voulez-vous le lancer? (o/n): ")
                if launch.lower() in ['o', 'oui', 'y', 'yes']:
                    from src.simple_server import run_server
                    run_server()
                    
        elif choice == "3":
            print("\nAu revoir! 👋")
            sys.exit(0)
            
        else:
            print("\nOption invalide. Veuillez choisir 1, 2 ou 3.")
            
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur. Au revoir!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF
