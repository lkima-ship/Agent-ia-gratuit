cat > run.py << 'EOF'
#!/usr/bin/env python3
"""
Point d'entrée principal de l'Agent IA Gratuit
"""

import sys
import os

def afficher_menu():
    print("\n" + "=" * 50)
    print("🤖 AGENT IA GRATUIT")
    print("=" * 50)
    print("1. Démarrer le serveur web")
    print("2. Voir la structure du projet")
    print("3. Tester le serveur")
    print("4. Quitter")
    print("=" * 50)

def demarrer_serveur():
    print("\n🚀 Démarrage du serveur web...")
    try:
        from src.simple_server import SimpleHandler
        from http.server import HTTPServer
        
        port = 8000
        server = HTTPServer(('0.0.0.0', port), SimpleHandler)
        print(f"✅ Serveur démarré sur http://localhost:{port}")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        server.serve_forever()
    except ImportError as e:
        print(f"❌ Erreur: {e}")
        print("Le fichier simple_server.py est peut-être manquant.")
    except KeyboardInterrupt:
        print("\n✅ Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")

def afficher_structure():
    print("\n📁 Structure du projet:")
    for root, dirs, files in os.walk("."):
        level = root.replace(".", "").count(os.sep)
        indent = "  " * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = "  " * (level + 1)
        for file in files:
            if file.endswith(".py"):
                print(f"{subindent}{file}")

def tester_serveur():
    print("\n🧪 Test du serveur...")
    import socket
    import time
    import subprocess
    
    # Vérifier si le port 8000 est libre
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    
    if result == 0:
        print("❌ Le port 8000 est déjà utilisé")
        return
    
    # Démarrer le serveur en arrière-plan
    print("🚀 Démarrage du serveur de test...")
    process = subprocess.Popen(
        [sys.executable, "src/simple_server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Attendre
    time.sleep(2)
    
    # Tester
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 8000))
    sock.close()
    
    if result == 0:
        print("✅ Le serveur fonctionne !")
    else:
        print("❌ Le serveur ne répond pas")
    
    # Arrêter le processus
    process.terminate()
    process.wait()

def main():
    while True:
        afficher_menu()
        
        try:
            choix = input("\nVotre choix (1-4): ").strip()
            
            if choix == "1":
                demarrer_serveur()
            elif choix == "2":
                afficher_structure()
            elif choix == "3":
                tester_serveur()
            elif choix == "4":
                print("\n👋 Au revoir !")
                sys.exit(0)
            else:
                print("\n❌ Choix invalide. Veuillez choisir 1-4.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir !")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erreur: {e}")

if __name__ == "__main__":
    main()
EOF
