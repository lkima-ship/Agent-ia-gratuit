cat > /root/agent_dashboard.py << 'EOF'
#!/usr/bin/env python3
"""
Dashboard web pour les agents IA avec API REST
"""

from flask import Flask, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

# Template HTML pour le dashboard
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard Agents IA</title>
    <meta charset="utf-8">
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
        .card { background: white; border-radius: 10px; padding: 20px; margin: 15px 0; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .agent { border-left: 4px solid #667eea; padding-left: 15px; }
        .btn { display: inline-block; padding: 10px 20px; background: #667eea; 
               color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
        .api-status { padding: 10px; border-radius: 5px; display: inline-block; }
        .online { background: #d4edda; color: #155724; }
        .offline { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Dashboard Agents IA</h1>
            <p>Système de gestion intégré - Port 5002</p>
            <div class="api-status {{ 'online' if api_online else 'offline' }}">
                API REST: {{ '✅ EN LIGNE' if api_online else '❌ HORS LIGNE' }}
            </div>
        </div>
        
        {% if api_online %}
        <div class="grid">
            <div class="card">
                <h2>📊 Vue système</h2>
                <p><strong>Agents:</strong> {{ system.agents_installed }}</p>
                <p><strong>Mémoire:</strong> {{ system.memory_usage }}</p>
                <p><strong>Disque:</strong> {{ system.disk_usage }}</p>
                <a href="/api/system/status" class="btn" target="_blank">Détails système</a>
            </div>
            
            <div class="card">
                <h2>🔗 Accès rapide</h2>
                <a href="/api/agents" class="btn" target="_blank">Liste agents</a>
                <a href="/api/docs" class="btn" target="_blank">Documentation API</a>
                <a href="/dashboard/json" class="btn">Vue JSON complète</a>
            </div>
        </div>
        
        <div class="card">
            <h2>🛠️ Scripts disponibles</h2>
            {% for script in scripts %}
            <form action="/execute/{{ script }}" method="post" style="display: inline;">
                <button type="submit" class="btn">{{ script }}</button>
            </form>
            {% endfor %}
        </div>
        
        <div class="card">
            <h2>🤖 Agents détectés ({{ agents|length }})</h2>
            {% for agent in agents %}
            <div class="agent">
                <h3>{{ agent.name }}</h3>
                <p>Taille: {{ agent.size }} octets • Lignes: {{ agent.lines }}</p>
                <a href="/api/agents/{{ agent.name }}" target="_blank" class="btn">Voir détails</a>
            </div>
            {% endfor %}
        </div>
        
        {% else %}
        <div class="card">
            <h2>⚠️ API non disponible</h2>
            <p>L'API REST sur le port 5002 n'est pas accessible.</p>
            <a href="/start" class="btn">Démarrer l'API</a>
        </div>
        {% endif %}
    </div>
</body>
</html>
"""

def check_api():
    """Vérifie si l'API est en ligne"""
    try:
        response = requests.get('http://localhost:5002/api/agents', timeout=2)
        return response.status_code == 200
    except:
        return False

@app.route('/')
def dashboard():
    """Page principale du dashboard"""
    api_online = check_api()
    
    if api_online:
        try:
            agents_resp = requests.get('http://localhost:5002/api/agents')
            system_resp = requests.get('http://localhost:5002/api/system/status')
            
            agents_data = agents_resp.json()
            system_data = system_resp.json()
            
            # Lister les scripts .sh
            scripts = [f for f in os.listdir('/root') if f.endswith('.sh') and not f.startswith('.')]
            
            return render_template_string(HTML_TEMPLATE,
                api_online=True,
                agents=agents_data.get('agents', []),
                system=system_data,
                scripts=scripts
            )
        except:
            api_online = False
    
    return render_template_string(HTML_TEMPLATE, api_online=False)

@app.route('/dashboard/json')
def dashboard_json():
    """Version JSON du dashboard"""
    try:
        agents = requests.get('http://localhost:5002/api/agents').json()
        system = requests.get('http://localhost:5002/api/system/status').json()
        return jsonify({
            "dashboard": "IA Agents Dashboard",
            "api_online": True,
            "agents": agents,
            "system": system,
            "scripts": [f for f in os.listdir('/root') if f.endswith('.sh')]
        })
    except:
        return jsonify({"api_online": False, "error": "API non disponible"})

@app.route('/start')
def start_api():
    """Démarre l'API"""
    os.system("cd /root && python3 api_rest_agents.py > /dev/null 2>&1 &")
    return "API démarrée en arrière-plan. <a href='/'>Retour</a>"

@app.route('/execute/<script>', methods=['POST'])
def execute(script):
    """Exécute un script via l'API"""
    try:
        response = requests.post(f'http://localhost:5002/api/execute/{script}')
        return f"""
        <div class="card">
            <h3>Résultat de l'exécution: {script}</h3>
            <pre>{response.text}</pre>
            <a href="/" class="btn">Retour</a>
        </div>
        """
    except:
        return "Erreur d'exécution"

if __name__ == '__main__':
    print("🌐 Dashboard Agents IA - http://localhost:5001")
    print("📊 API REST principale - http://localhost:5002")
    app.run(host='0.0.0.0', port=5001, debug=False)
EOF
