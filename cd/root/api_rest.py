cat > /root/api_rest.py << 'EOF'
#!/usr/bin/env python3
"""
API REST complète pour le système d'agents IA
Version: 2.0
"""
from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys
import json
import subprocess
import psutil
from datetime import datetime
import threading
import time

# Initialisation
app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Variables globales
AGENTS_BASE_DIR = "/root"
RUNNING_AGENTS = {}
API_KEYS = {
    "admin": "admin_key_123",
    "user": "user_key_456"
}

# HTML pour l'interface web
API_DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>🔌 API REST - Système d'Agents IA</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        
        .header h1 {
            color: #2d3436;
            margin-bottom: 10px;
            font-size: 2.5rem;
        }
        
        .header p {
            color: #636e72;
            font-size: 1.1rem;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-card h3 {
            color: #636e72;
            font-size: 1rem;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card .value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #6c5ce7;
        }
        
        .endpoints {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .endpoint {
            background: #f8f9fa;
            border-left: 4px solid #6c5ce7;
            padding: 20px;
            margin-bottom: 15px;
            border-radius: 0 8px 8px 0;
        }
        
        .method {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
            margin-right: 10px;
        }
        
        .method.get { background: #61affe; color: white; }
        .method.post { background: #49cc90; color: white; }
        .method.put { background: #fca130; color: white; }
        .method.delete { background: #f93e3e; color: white; }
        
        .path {
            font-family: 'Courier New', monospace;
            background: #2d3436;
            color: white;
            padding: 8px 15px;
            border-radius: 5px;
            margin: 10px 0;
            display: inline-block;
        }
        
        .description {
            color: #636e72;
            margin-top: 10px;
        }
        
        .try-it {
            background: #6c5ce7;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
            font-weight: bold;
            transition: background 0.3s;
        }
        
        .try-it:hover {
            background: #5b4bd8;
        }
        
        .api-key {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        .key-display {
            background: #2d3436;
            color: white;
            padding: 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            margin: 15px 0;
            word-break: break-all;
        }
        
        .footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 0.9rem;
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background: #00b894; }
        .status-offline { background: #d63031; }
        
        @media (max-width: 768px) {
            .container { padding: 10px; }
            .header { padding: 20px; }
            .header h1 { font-size: 2rem; }
            .stat-card .value { font-size: 2rem; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔌 API REST - Système d'Agents IA</h1>
            <p>Contrôlez votre écosystème d'agents via des requêtes HTTP</p>
            <div style="margin-top: 15px;">
                <span class="status-indicator status-online"></span>
                <strong>API Status: <span id="apiStatus">ONLINE</span></strong>
            </div>
        </div>
        
        <div class="stats" id="statsContainer">
            <!-- Les stats seront chargées via JavaScript -->
        </div>
        
        <div class="endpoints">
            <h2 style="margin-bottom: 20px; color: #2d3436;">📡 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <div class="path">/api/status</div>
                <div class="description">Obtenir le statut du système et les statistiques</div>
                <button class="try-it" onclick="testEndpoint('/api/status', 'GET')">Tester</button>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <div class="path">/api/agents</div>
                <div class="description">Lister tous les agents disponibles par catégorie</div>
                <button class="try-it" onclick="testEndpoint('/api/agents', 'GET')">Tester</button>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <div class="path">/api/agents/<category></div>
                <div class="description">Lister les agents d'une catégorie spécifique</div>
                <button class="try-it" onclick="testEndpoint('/api/agents/WEB', 'GET')">Tester WEB</button>
                <button class="try-it" onclick="testEndpoint('/api/agents/IA', 'GET')">Tester IA</button>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <div class="path">/api/agent/run</div>
                <div class="description">Lancer un agent (body: {"agent": "nom_agent.py"})</div>
                <button class="try-it" onclick="testRunAgent()">Tester</button>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <div class="path">/api/processes</div>
                <div class="description">Voir les agents actuellement en cours d'exécution</div>
                <button class="try-it" onclick="testEndpoint('/api/processes', 'GET')">Tester</button>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <div class="path">/api/agent/stop</div>
                <div class="description">Arrêter un agent (body: {"pid": 12345})</div>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <div class="path">/api/docs</div>
                <div class="description">Documentation complète de l'API au format JSON</div>
                <button class="try-it" onclick="testEndpoint('/api/docs', 'GET')">Tester</button>
            </div>
        </div>
        
        <div class="api-key">
            <h2 style="margin-bottom: 20px; color: #2d3436;">🔑 Clés API</h2>
            <p>Utilisez cette clé pour les requêtes nécessitant une authentification :</p>
            <div class="key-display" id="apiKeyDisplay">admin_key_123</div>
            <p>Header: <code>X-API-Key: admin_key_123</code></p>
            <small style="color: #636e72;">Note: En production, utilisez des clés sécurisées et un système d'authentification.</small>
        </div>
    </div>
    
    <div class="footer">
        <p>Système d'Agents IA &copy; 2024 | API REST v2.0</p>
        <p>Dernière mise à jour: {{ update_time }}</p>
    </div>
    
    <script>
        // Fonction pour charger les statistiques
        async function loadStats() {
            try {
                const response = await fetch('/api/status');
                const data = await response.json();
                
                const statsContainer = document.getElementById('statsContainer');
                statsContainer.innerHTML = `
                    <div class="stat-card">
                        <h3>Agents Disponibles</h3>
                        <div class="value">${data.stats.total_agents || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Catégories</h3>
                        <div class="value">${data.stats.total_categories || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Agents Actifs</h3>
                        <div class="value">${data.stats.running_agents || 0}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Fichiers Python</h3>
                        <div class="value">${data.stats.total_python_files || 0}</div>
                    </div>
                `;
            } catch (error) {
                console.error('Erreur lors du chargement des stats:', error);
            }
        }
        
        // Fonction pour tester un endpoint
        async function testEndpoint(endpoint, method) {
            try {
                const response = await fetch(endpoint, {
                    method: method,
                    headers: {
                        'X-API-Key': 'admin_key_123'
                    }
                });
                
                const data = await response.json();
                alert(`Réponse de ${endpoint}:\n\n${JSON.stringify(data, null, 2)}`);
            } catch (error) {
                alert(`Erreur avec ${endpoint}: ${error.message}`);
            }
        }
        
        // Fonction pour tester le lancement d'un agent
        async function testRunAgent() {
            const agentName = prompt("Nom de l'agent à lancer (ex: agent_web_avance.py):");
            if (!agentName) return;
            
            try {
                const response = await fetch('/api/agent/run', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-API-Key': 'admin_key_123'
                    },
                    body: JSON.stringify({ agent: agentName })
                });
                
                const data = await response.json();
                alert(`Réponse:\n\n${JSON.stringify(data, null, 2)}`);
            } catch (error) {
                alert(`Erreur: ${error.message}`);
            }
        }
        
        // Charger les stats au démarrage
        document.addEventListener('DOMContentLoaded', loadStats);
        
        // Rafraîchir les stats toutes les 30 secondes
        setInterval(loadStats, 30000);
    </script>
</body>
</html>
'''

# ==================== FONCTIONS UTILITAIRES ====================

def get_agent_categories():
    """Récupère toutes les catégories d'agents disponibles"""
    categories = {}
    try:
        for item in os.listdir(AGENTS_BASE_DIR):
            item_path = os.path.join(AGENTS_BASE_DIR, item)
            if os.path.isdir(item_path) and item.isupper():
                agents = []
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        if file.endswith('.py'):
                            agents.append({
                                'name': file,
                                'path': os.path.join(root, file),
                                'relative_path': os.path.relpath(os.path.join(root, file), AGENTS_BASE_DIR)
                            })
                if agents:
                    categories[item] = agents
    except Exception as e:
        print(f"Erreur lors de la lecture des catégories: {e}")
    
    return categories

def get_running_agents():
    """Récupère la liste des agents Python en cours d'exécution"""
    running = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                cmdline = proc.info['cmdline']
                if cmdline and 'python' in cmdline[0]:
                    # Cherche si c'est un de nos agents
                    for part in cmdline:
                        if part.endswith('.py') and AGENTS_BASE_DIR in part:
                            running.append({
                                'pid': proc.info['pid'],
                                'name': os.path.basename(part),
                                'path': part,
                                'start_time': datetime.fromtimestamp(proc.info['create_time']).strftime('%Y-%m-%d %H:%M:%S'),
                                'status': 'running'
                            })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except Exception as e:
        print(f"Erreur lors de la récupération des processus: {e}")
    
    return running

def count_python_files():
    """Compte tous les fichiers Python dans le système"""
    count = 0
    try:
        for root, dirs, files in os.walk(AGENTS_BASE_DIR):
            count += len([f for f in files if f.endswith('.py')])
    except:
        pass
    return count

# ==================== MIDDLEWARE D'AUTHENTIFICATION ====================

def require_api_key(func):
    """Décorateur pour vérifier la clé API"""
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key in API_KEYS.values():
            return func(*args, **kwargs)
        return jsonify({
            'error': 'Accès non autorisé',
            'message': 'Clé API manquante ou invalide'
        }), 401
    wrapper.__name__ = func.__name__
    return wrapper

# ==================== ROUTES DE L'API ====================

@app.route('/')
def api_dashboard():
    """Page d'accueil de l'API avec interface web"""
    update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render_template_string(API_DASHBOARD_HTML, update_time=update_time)

@app.route('/api/status', methods=['GET'])
@limiter.exempt
def api_status():
    """Endpoint: Statut du système"""
    categories = get_agent_categories()
    running_agents = get_running_agents()
    
    stats = {
        'system': {
            'hostname': os.uname().nodename if hasattr(os, 'uname') else 'Unknown',
            'python_version': sys.version,
            'platform': sys.platform,
            'timestamp': datetime.now().isoformat()
        },
        'stats': {
            'total_categories': len(categories),
            'total_agents': sum(len(agents) for agents in categories.values()),
            'running_agents': len(running_agents),
            'total_python_files': count_python_files()
        },
        'categories': list(categories.keys())
    }
    
    return jsonify(stats)

@app.route('/api/agents', methods=['GET'])
@require_api_key
def list_all_agents():
    """Endpoint: Liste tous les agents par catégorie"""
    categories = get_agent_categories()
    return jsonify(categories)

@app.route('/api/agents/<category>', methods=['GET'])
@require_api_key
def list_category_agents(category):
    """Endpoint: Liste les agents d'une catégorie spécifique"""
    category_path = os.path.join(AGENTS_BASE_DIR, category)
    
    if not os.path.exists(category_path):
        return jsonify({
            'error': 'Catégorie non trouvée',
            'available_categories': list(get_agent_categories().keys())
        }), 404
    
    agents = []
    for root, dirs, files in os.walk(category_path):
        for file in files:
            if file.endswith('.py'):
                agents.append({
                    'name': file,
                    'path': os.path.join(root, file),
                    'size': os.path.getsize(os.path.join(root, file)),
                    'modified': datetime.fromtimestamp(
                        os.path.getmtime(os.path.join(root, file))
                    ).isoformat()
                })
    
    return jsonify({
        'category': category,
        'count': len(agents),
        'agents': agents
    })

@app.route('/api/agent/run', methods=['POST'])
@require_api_key
def run_agent():
    """Endpoint: Lancer un agent"""
    data = request.json
    
    if not data or 'agent' not in data:
        return jsonify({
            'error': 'Paramètre manquant',
            'message': 'Le paramètre "agent" est requis'
        }), 400
    
    agent_name = data['agent']
    
    # Chercher l'agent dans toutes les catégories
    agent_path = None
    categories = get_agent_categories()
    
    for category, agents in categories.items():
        for agent in agents:
            if agent['name'] == agent_name:
                agent_path = agent['path']
                break
        if agent_path:
            break
    
    # Si non trouvé dans les catégories, chercher à la racine
    if not agent_path and os.path.exists(os.path.join(AGENTS_BASE_DIR, agent_name)):
        agent_path = os.path.join(AGENTS_BASE_DIR, agent_name)
    
    if not agent_path or not os.path.exists(agent_path):
        return jsonify({
            'error': 'Agent non trouvé',
            'available_agents': [agent['name'] for agents in categories.values() for agent in agents[:50]]
        }), 404
    
    try:
        # Lancer l'agent en arrière-plan
        process = subprocess.Popen(
            [sys.executable, agent_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Stocker les informations du processus
        RUNNING_AGENTS[process.pid] = {
            'agent': agent_name,
            'process': process,
            'start_time': datetime.now().isoformat(),
            'path': agent_path
        }
        
        return jsonify({
            'success': True,
            'message': f'Agent {agent_name} lancé avec succès',
            'pid': process.pid,
            'details': {
                'agent': agent_name,
                'path': agent_path,
                'start_time': datetime.now().isoformat()
            }
        })
    
    except Exception as e:
        return jsonify({
            'error': 'Erreur lors du lancement',
            'message': str(e)
        }), 500

@app.route('/api/processes', methods=['GET'])
@require_api_key
def list_processes():
    """Endpoint: Lister les processus en cours"""
    running_agents = get_running_agents()
    
    return jsonify({
        'count': len(running_agents),
        'processes': running_agents
    })

@app.route('/api/agent/stop', methods=['POST'])
@require_api_key
def stop_agent():
    """Endpoint: Arrêter un agent"""
    data = request.json
    
    if not data or 'pid' not in data:
        return jsonify({
            'error': 'Paramètre manquant',
            'message': 'Le paramètre "pid" est requis'
        }), 400
    
    pid = int(data['pid'])
    
    try:
        process = psutil.Process(pid)
        process.terminate()
        
        # Attendre un peu pour la terminaison
        try:
            process.wait(timeout=5)
        except:
            process.kill()
        
        if pid in RUNNING_AGENTS:
            del RUNNING_AGENTS[pid]
        
        return jsonify({
            'success': True,
            'message': f'Processus {pid} arrêté avec succès'
        })
    
    except psutil.NoSuchProcess:
        return jsonify({
            'error': 'Processus non trouvé',
            'message': f'Le processus avec PID {pid} n\'existe pas'
        }), 404
    
    except Exception as e:
        return jsonify({
            'error': 'Erreur lors de l\'arrêt',
            'message': str(e)
        }), 500

@app.route('/api/docs', methods=['GET'])
@limiter.exempt
def api_documentation():
    """Endpoint: Documentation complète de l'API"""
    docs = {
        'api': {
            'name': 'API REST - Système d\'Agents IA',
            'version': '2.0',
            'description': 'API permettant de contrôler et gérer un écosystème d\'agents IA',
            'base_url': 'http://localhost:5002',
            'authentication': 'Clé API via header X-API-Key'
        },
        'endpoints': [
            {
                'method': 'GET',
                'path': '/',
                'description': 'Interface web du tableau de bord API',
                'authentication': 'Non requise'
            },
            {
                'method': 'GET',
                'path': '/api/status',
                'description': 'Statut du système et statistiques',
                'authentication': 'Non requise',
                'response': {
                    'system': 'Informations système',
                    'stats': 'Statistiques des agents',
                    'categories': 'Liste des catégories'
                }
            },
            {
                'method': 'GET',
                'path': '/api/agents',
                'description': 'Liste tous les agents par catégorie',
                'authentication': 'Requise',
                'headers': {
                    'X-API-Key': 'Clé API valide'
                }
            },
            {
                'method': 'GET',
                'path': '/api/agents/<category>',
                'description': 'Liste les agents d\'une catégorie spécifique',
                'authentication': 'Requise',
                'parameters': {
                    'category': 'Nom de la catégorie (ex: WEB, IA)'
                }
            },
            {
                'method': 'POST',
                'path': '/api/agent/run',
                'description': 'Lance un agent',
                'authentication': 'Requise',
                'body': {
                    'agent': 'Nom du fichier agent (ex: agent_web_avance.py)'
                }
            },
            {
                'method': 'GET',
                'path': '/api/processes',
                'description': 'Liste les agents en cours d\'exécution',
                'authentication': 'Requise'
            },
            {
                'method': 'POST',
                'path': '/api/agent/stop',
                'description': 'Arrête un agent',
                'authentication': 'Requise',
                'body': {
                    'pid': 'PID du processus à arrêter'
                }
            },
            {
                'method': 'GET',
                'path': '/api/docs',
                'description': 'Documentation complète de l\'API',
                'authentication': 'Non requise'
            }
        ],
        'clés_api': {
            'admin': 'admin_key_123',
            'user': 'user_key_456'
        }
    }
    
    return jsonify(docs)

@app.route('/api/search', methods=['GET'])
@require_api_key
def search_agents():
    """Endpoint: Recherche d'agents par mot-clé"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({
            'error': 'Paramètre manquant',
            'message': 'Le paramètre de recherche "q" est requis'
        }), 400
    
    results = []
    categories = get_agent_categories()
    
    for category, agents in categories.items():
        for agent in agents:
            if query.lower() in agent['name'].lower():
                results.append({
                    'category': category,
                    'agent': agent['name'],
                    'path': agent['relative_path']
                })
    
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })

# ==================== GESTIONNAIRE D'ERREURS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint non trouvé',
        'message': 'La ressource demandée n\'existe pas'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'error': 'Méthode non autorisée',
        'message': 'La méthode HTTP utilisée n\'est pas supportée pour cette ressource'
    }), 405

@app.errorhandler(429)
def ratelimit_handler(error):
    return jsonify({
        'error': 'Trop de requêtes',
        'message': 'Vous avez dépassé le nombre maximum de requêtes autorisées'
    }), 429

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Erreur interne du serveur',
        'message': 'Une erreur s\'est produite lors du traitement de votre requête'
    }), 500

# ==================== FONCTION PRINCIPALE ====================

def start_api_server(port=5002, debug=False):
    """Lance le serveur API"""
    print(f"""
    🌐 API REST - Système d'Agents IA
    {'='*50}
    
    📊 Statut du système:
      • Catégories détectées: {len(get_agent_categories())}
      • Agents disponibles: {sum(len(agents) for agents in get_agent_categories().values())}
      • Agents en cours d'exécution: {len(get_running_agents())}
    
    🔑 Clés API disponibles:
      • Admin: admin_key_123
      • User: user_key_456
    
    🚀 Endpoints:
      • Dashboard: http://localhost:{port}/
      • API Status: http://localhost:{port}/api/status
      • Documentation: http://localhost:{port}/api/docs
    
    📡 Le serveur écoute sur le port {port}
    ℹ️  Appuyez sur Ctrl+C pour arrêter le serveur
    {'='*50}
    """)
    
    app.run(host='0.0.0.0', port=port, debug=debug, threaded=True)

if __name__ == '__main__':
    start_api_server(port=5002, debug=False)
EOF
