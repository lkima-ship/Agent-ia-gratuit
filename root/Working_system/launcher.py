# Crée ce fichier à la place de run.py
cat > /root/working_system/launcher.py << 'EOF'
#!/usr/bin/env python3
"""
Launcher intelligent pour le système IA
"""
import sys
import os
import subprocess
import time

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print("=" * 50)
    print("🤖  SYSTÈME IA COMPLET - Alpine Linux")
    print("=" * 50)

def run_agent():
    print("🤖 Lancement de SuperAgent...")
    subprocess.Popen([sys.executable, "-c", "from super_agent import SuperAgent; agent = SuperAgent(); agent.run()"])

def run_api():
    print("🔌 Lancement de l'API REST...")
    subprocess.Popen([sys.executable, "-c", "from api_rest import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=5000)"])

def run_dashboard():
    print("📊 Lancement du Dashboard...")
    # Vérifier si Dashboard.py existe et est exécutable
    if os.path.exists("Dashboard.py"):
        subprocess.Popen([sys.executable, "Dashboard.py"])
    else:
        print("❌ Dashboard.py non trouvé, création d'une version simple...")
        # Créer un dashboard simple
        with open("Dashboard_simple.py", "w") as f:
            f.write('''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "<h1>Dashboard IA</h1><p>Système en fonctionnement</p>"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
''')
        subprocess.Popen([sys.executable, "Dashboard_simple.py"])

def check_services():
    print("\n🔍 Vérification des services...")
    os.system("netstat -tuln | grep -E ':5000|:8000' || echo 'Aucun service détecté'")

def main():
    while True:
        print_header()
        print("\nMenu Principal:")
        print("1. 🚀 Lancer TOUT (API + Dashboard + Agent)")
        print("2. 🤖 Lancer seulement l'Agent IA")
        print("3. 🔌 Lancer seulement l'API REST")
        print("4. 📊 Lancer seulement le Dashboard")
        print("5. 🔍 Vérifier les services en cours")
        print("6. 🛑 Arrêter tous les services")
        print("0. ❌ Quitter")
        
        choice = input("\nVotre choix: ")
        
        if choice == "1":
            print("\n🚀 Lancement complet du système...")
            run_api()
            time.sleep(2)
            run_dashboard()
            time.sleep(2)
            run_agent()
            print("\n✅ Tous les services ont été démarrés!")
            print("🔌 API:      http://localhost:5000")
            print("📊 Dashboard: http://localhost:8000")
            
        elif choice == "2":
            run_agent()
            
        elif choice == "3":
            run_api()
            
        elif choice == "4":
            run_dashboard()
            
        elif choice == "5":
            check_services()
            
        elif choice == "6":
            os.system("pkill -f python3")
            print("✅ Tous les services Python ont été arrêtés.")
            
        elif choice == "0":
            print("\n👋 Au revoir!")
            break
            
        else:
            print("❌ Choix invalide!")
        
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF

# Lance le nouveau launcher
cd /root/working_system
python3 launcher.py
