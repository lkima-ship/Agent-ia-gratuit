cat > /root/setup_ia_system.sh << 'EOF'
#!/bin/bash
echo "🚀 Installation du système IA complet..."

# Créer le dossier principal
mkdir -p /root/ia_system
cd /root/ia_system

echo "📁 Création des fichiers..."

# 1. Créer l'API
cat > api.py << 'API_EOF'
#!/usr/bin/env python3
from flask import Flask, jsonify
import time

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "service": "AI System API",
        "version": "1.0",
        "time": time.time()
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/agents')
def agents():
    return jsonify({
        "agents": ["SuperAgent", "Cognitive", "DataAnalyzer"],
        "count": 3
    })

if __name__ == '__main__':
    print("🔌 API démarrée: http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)
API_EOF

# 2. Créer l'Agent intelligent
cat > agent.py << 'AGENT_EOF'
#!/usr/bin/env python3
import time
import os
import sys

class AIAgent:
    def __init__(self, name="AI_Agent"):
        self.name = name
        self.version = "2.0"
        self.log_file = "/root/ia_system/agent.log"
        
    def log(self, message):
        """Écrire dans le fichier log"""
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        
        with open(self.log_file, 'a') as f:
            f.write(log_line + '\n')
        
        # Afficher seulement si lancé manuellement
        if os.isatty(sys.stdout.fileno()):
            print(log_line)
    
    def run(self):
        self.log(f"🤖 {self.name} v{self.version} démarré")
        self.log(f"📁 Répertoire: {os.getcwd()}")
        self.log(f"🐍 Python: {sys.version.split()[0]}")
        
        counter = 0
        try:
            while True:
                counter += 1
                self.log(f"Cycle {counter} - En fonctionnement")
                time.sleep(10)
                
        except KeyboardInterrupt:
            self.log("🛑 Agent arrêté par l'utilisateur")
        except Exception as e:
            self.log(f"❌ Erreur: {e}")

# Version simple pour exécution directe
if __name__ == "__main__":
    agent = AIAgent()
    agent.run()
AGENT_EOF

# 3. Créer le Dashboard
cat > dashboard.py << 'DASH_EOF'
#!/usr/bin/env python3
from flask import Flask, render_template_string
import os
import platform

app = Flask(__name__)
app.config['DEBUG'] = False

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Dashboard</title>
    <meta charset="utf-8">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: white;
        }
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            color: #333;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .status-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #4CAF50;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }
        .status-card.offline {
            border-left-color: #f44336;
        }
        .status {
            font-weight: bold;
            font-size: 18px;
        }
        .online { color: #4CAF50; }
        .offline { color: #f44336; }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: #667eea;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 5px;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
        .log-window {
            background: #1a1a1a;
            color: #00ff00;
            padding: 15px;
            border-radius: 5px;
            font-family: monospace;
            max-height: 300px;
            overflow-y: auto;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Système IA - Tableau de bord</h1>
            <p>Alpine Linux • Contrôle et surveillance</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🔌 API REST</h3>
                <p class="status online">● En ligne</p>
                <p>Port: 5000</p>
                <a href="http://localhost:5000" target="_blank" class="btn">Accéder</a>
            </div>
            
            <div class="status-card">
                <h3>🤖 Agent IA</h3>
                <p class="status online">● Actif</p>
                <p>SuperAgent v2.0</p>
                <a href="/logs" class="btn">Voir logs</a>
            </div>
            
            <div class="status-card">
                <h3>📊 Dashboard</h3>
                <p class="status online">● En cours</p>
                <p>Port: 8000</p>
                <a href="/system" class="btn">Info système</a>
            </div>
        </div>
        
        <h2>📈 Logs en temps réel</h2>
        <div class="log-window">
            {{ logs|safe }}
        </div>
        
        <div style="margin-top: 30px; text-align: center;">
            <a href="/api" class="btn">API Documentation</a>
            <a href="/control" class="btn">Contrôle</a>
            <a href="/system" class="btn">Système</a>
            <a href="/restart" class="btn">Redémarrer</a>
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Lire les logs
    logs = "Chargement des logs..."
    try:
        with open('/root/ia_system/agent.log', 'r') as f:
            logs = f.read()[-1500:]  # 1500 derniers caractères
    except:
        logs = "Aucun log disponible"
    
    return render_template_string(HTML_TEMPLATE, logs=logs)

@app.route('/logs')
def logs():
    try:
        with open('/root/ia_system/agent.log', 'r') as f:
            content = f.read()
        return f'<pre style="background:#000;color:#0f0;padding:20px;">{content}</pre>'
    except:
        return '<pre>Aucun log trouvé</pre>'

@app.route('/api')
def api():
    return '''
    <h1>API Documentation</h1>
    <ul>
        <li><a href="http://localhost:5000" target="_blank">GET /</a> - Statut API</li>
        <li><a href="http://localhost:5000/health" target="_blank">GET /health</a> - Santé</li>
        <li><a href="http://localhost:5000/agents" target="_blank">GET /agents</a> - Agents</li>
    </ul>
    '''

@app.route('/system')
def system_info():
    import platform
    info = f"""
    <h1>Informations système</h1>
    <pre>
    Système: {platform.system()} {platform.release()}
    Python: {platform.python_version()}
    Processeur: {platform.processor()}
    Répertoire: {os.getcwd()}
    </pre>
    """
    return info

@app.route('/control')
def control():
    return '''
    <h1>Contrôle du système</h1>
    <p>Fonctions de contrôle à venir...</p>
    '''

@app.route('/restart')
def restart():
    return '''
    <h1>Redémarrage</h1>
    <p>Cette fonctionnalité sera implémentée prochainement.</p>
    '''

if __name__ == '__main__':
    print("📊 Dashboard démarré: http://0.0.0.0:8000")
    print("🌐 Ouvrez votre navigateur à cette adresse")
    app.run(host='0.0.0.0', port=8000, debug=False)
DASH_EOF

# 4. Créer le menu principal SIMPLE
cat > menu.py << 'MENU_EOF'
#!/usr/bin/env python3
"""
Menu principal SIMPLE et FONCTIONNEL
"""
import os
import sys
import subprocess
import time
import signal

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header():
    clear_screen()
    print("═" * 50)
    print("           🤖 SYSTÈME IA - ALPINE LINUX")
    print("═" * 50)

def check_port(port):
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        return result == 0
    except:
        return False

def show_status():
    print("\n📊 ÉTAT DES SERVICES:")
    print("-" * 40)
    
    # Vérifier API
    if check_port(5000):
        print("🔌 API (port 5000):      ✅ EN LIGNE")
    else:
        print("🔌 API (port 5000):      ❌ HORS LIGNE")
    
    # Vérifier Dashboard
    if check_port(8000):
        print("📊 Dashboard (port 8000): ✅ EN LIGNE")
    else:
        print("📊 Dashboard (port 8000): ❌ HORS LIGNE")
    
    # Vérifier Agent
    try:
        output = os.popen("ps aux | grep 'python3.*agent.py' | grep -v grep").read()
        if "agent.py" in output:
            print("🤖 Agent IA:            ✅ ACTIF")
        else:
            print("🤖 Agent IA:            ❌ INACTIF")
    except:
        print("🤖 Agent IA:            ❓ INCONNU")

def start_api():
    print("🚀 Démarrage de l'API...")
    subprocess.Popen([sys.executable, "api.py"], 
                    stdout=open('/root/ia_system/api.log', 'w'),
                    stderr=subprocess.STDOUT)
    time.sleep(3)
    if check_port(5000):
        print("✅ API démarrée: http://localhost:5000")
    else:
        print("⚠️  API peut-être en cours de démarrage...")

def start_dashboard():
    print("🚀 Démarrage du Dashboard...")
    subprocess.Popen([sys.executable, "dashboard.py"],
                    stdout=open('/root/ia_system/dashboard.log', 'w'),
                    stderr=subprocess.STDOUT)
    time.sleep(3)
    if check_port(8000):
        print("✅ Dashboard démarré: http://localhost:8000")
    else:
        print("⚠️  Dashboard peut-être en cours de démarrage...")

def start_agent():
    print("🚀 Démarrage de l'Agent...")
    subprocess.Popen([sys.executable, "agent.py"],
                    stdout=open('/root/ia_system/agent_output.log', 'a'),
                    stderr=subprocess.STDOUT)
    print("✅ Agent démarré en arrière-plan")
    print("📝 Logs: /root/ia_system/agent.log")

def stop_all():
    print("🛑 Arrêt de tous les services...")
    
    # Tuer les processus par port
    for port in [5000, 8000]:
        try:
            output = os.popen(f"lsof -ti:{port}").read()
            if output:
                os.system(f"kill -9 {output} 2>/dev/null")
        except:
            pass
    
    # Tuer les processus par nom
    os.system("pkill -f 'python3.*(api.py|dashboard.py|agent.py)' 2>/dev/null")
    
    time.sleep(2)
    print("✅ Tous les services arrêtés")

def show_logs():
    print("\n📜 LOGS RÉCENTS:")
    print("-" * 60)
    try:
        with open('/root/ia_system/agent.log', 'r') as f:
            lines = f.readlines()[-10:]
            for line in lines:
                print(line.rstrip())
    except:
        print("Aucun log disponible")
    
    input("\nAppuyez sur Entrée pour continuer...")

def main():
    while True:
        print_header()
        show_status()
        
        print("\n📋 MENU PRINCIPAL:")
        print("1. 🚀 Lancer TOUT (API + Dashboard + Agent)")
        print("2. 🔌 Lancer l'API seule")
        print("3. 📊 Lancer le Dashboard seul")
        print("4. 🤖 Lancer l'Agent seul")
        print("5. 📜 Afficher les logs")
        print("6. 🛑 Arrêter TOUT")
        print("7. ❌ Quitter")
        print("-" * 50)
        
        try:
            choice = input("\nVotre choix [1-7]: ").strip()
            
            if choice == "1":
                stop_all()
                time.sleep(2)
                start_api()
                time.sleep(2)
                start_dashboard()
                time.sleep(2)
                start_agent()
                print("\n✅ Tous les services démarrés!")
                print("🔌 API:      http://localhost:5000")
                print("📊 Dashboard: http://localhost:8000")
                print("🤖 Agent:    En arrière-plan")
                input("\nAppuyez sur Entrée pour continuer...")
            
            elif choice == "2":
                start_api()
                time.sleep(2)
            
            elif choice == "3":
                start_dashboard()
                time.sleep(2)
            
            elif choice == "4":
                start_agent()
                time.sleep(2)
            
            elif choice == "5":
                show_logs()
            
            elif choice == "6":
                stop_all()
                time.sleep(2)
            
            elif choice == "7":
                stop_all()
                print("\n👋 Au revoir!")
                break
            
            else:
                print("❌ Choix invalide!")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interruption détectée!")
            confirm = input("Arrêter tout et quitter? (o/n): ").lower()
            if confirm == 'o':
                stop_all()
                break

if __name__ == "__main__":
    main()
MENU_EOF

# 5. Créer les scripts de démarrage/arrêt
cat > start.sh << 'START_EOF'
#!/bin/bash
cd /root/ia_system
python3 menu.py
START_EOF

cat > stop.sh << 'STOP_EOF'
#!/bin/bash
echo "🛑 Arrêt du système IA..."
cd /root/ia_system

# Arrêter les processus
pkill -f "python3.*(api.py|dashboard.py|agent.py)" 2>/dev/null

# Libérer les ports
for port in 5000 8000; do
    lsof -ti:$port 2>/dev/null | xargs kill -9 2>/dev/null
done

echo "✅ Système arrêté"
STOP_EOF

# 6. Rendre tout exécutable
chmod +x api.py dashboard.py agent.py menu.py start.sh stop.sh

# 7. Créer un fichier de log initial
echo "[$(date)] Système IA installé" > agent.log

echo ""
echo "✅ INSTALLATION TERMINÉE !"
echo ""
echo "📍 Répertoire: /root/ia_system"
echo ""
echo "📁 Fichiers créés:"
echo "   api.py       - API REST (port 5000)"
echo "   agent.py     - Agent IA (logs dans agent.log)"
echo "   dashboard.py - Interface web (port 8000)"
echo "   menu.py      - Menu de contrôle"
echo "   start.sh     - Script de démarrage"
echo "   stop.sh      - Script d'arrêt"
echo ""
echo "🚀 Pour démarrer:"
echo "   cd /root/ia_system"
echo "   ./start.sh"
echo "   ou"
echo "   python3 menu.py"
echo ""
echo "🌐 Accès web:"
echo "   API:      http://localhost:5000"
echo "   Dashboard: http://localhost:8000"
EOF

# Rendre le script exécutable
chmod +x /root/setup_ia_system.sh

# Exécuter l'installation
/root/setup_ia_system.sh
