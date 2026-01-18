# Créer une version adaptée aux agents IA
cat > /root/api_rest_agents.py << 'EOF'
#!/usr/bin/env python3
"""
API REST pour le système d'agents IA
Intégration avec les agents existants
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import json
import socket

app = Flask(__name__)
CORS(app)

# Chemin vers vos fichiers
AGENTS_DIR = "/root"

def list_agents():
    """Liste tous les agents disponibles"""
    agents = []
    for file in os.listdir(AGENTS_DIR):
        if file.endswith('.py') and 'agent' in file.lower():
            agents.append({
                "name": file,
                "path": os.path.join(AGENTS_DIR, file),
                "size": os.path.getsize(os.path.join(AGENTS_DIR, file))
            })
    return agents

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """Liste tous les agents IA"""
    return jsonify({
        "system": "IA Agents System",
        "hostname": socket.gethostname(),
        "total_agents": len(list_agents()),
        "agents": list_agents(),
        "scripts": [f for f in os.listdir(AGENTS_DIR) if f.endswith('.sh')]
    })

@app.route('/api/agents/<agent_name>', methods=['GET'])
def get_agent_info(agent_name):
    """Informations sur un agent spécifique"""
    agent_path = os.path.join(AGENTS_DIR, agent_name)
    if not os.path.exists(agent_path):
        return jsonify({"error": "Agent non trouvé"}), 404
    
    with open(agent_path, 'r') as f:
        content = f.read(2000)  # Premières 2000 caractères
    
    return jsonify({
        "name": agent_name,
        "exists": True,
        "size": os.path.getsize(agent_path),
        "preview": content,
        "lines": sum(1 for _ in open(agent_path))
    })

@app.route('/api/system/status', methods=['GET'])
def system_status():
    """Statut du système complet"""
    processes = []
    try:
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        processes = [line for line in result.stdout.split('\n') if 'python' in line or 'agent' in line][:10]
    except:
        pass
    
    return jsonify({
        "status": "running",
        "agents_installed": len(list_agents()),
        "active_processes": len(processes),
        "memory_usage": subprocess.getoutput("free -m | awk 'NR==2{printf \"%s/%sMB (%.2f%%)\", $3,$2,$3*100/$2 }'"),
        "disk_usage": subprocess.getoutput("df -h | awk '$NF==\"/\"{printf \"%d/%dGB (%s)\", $3,$2,$5}'"),
        "top_processes": processes
    })

@app.route('/api/execute/<script>', methods=['POST'])
def execute_script(script):
    """Exécute un script (avec restrictions)"""
    allowed_scripts = ['check_system.sh', 'verifier_agents.sh', 'organize_agent.sh']
    
    if script not in allowed_scripts:
        return jsonify({"error": "Script non autorisé"}), 403
    
    script_path = os.path.join(AGENTS_DIR, script)
    if not os.path.exists(script_path):
        return jsonify({"error": "Script non trouvé"}), 404
    
    try:
        result = subprocess.run(
            ['bash', script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return jsonify({
            "script": script,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Timeout - script trop long"}), 408
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/docs', methods=['GET'])
def documentation():
    """Documentation de l'API Agents"""
    return jsonify({
        "api": "IA Agents REST API",
        "version": "2.0.0",
        "endpoints": {
            "/api/agents": "Liste tous les agents",
            "/api/agents/<name>": "Détails d'un agent",
            "/api/system/status": "Statut système complet",
            "/api/execute/<script>": "Exécute un script (sécurisé)"
        },
        "available_scripts": ['check_system.sh', 'verifier_agents.sh', 'organize_agent.sh']
    })

if __name__ == '__main__':
    print("🔗 API REST Agents IA - Port 5002")
    print("📁 Agents détectés:", len(list_agents()))
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
