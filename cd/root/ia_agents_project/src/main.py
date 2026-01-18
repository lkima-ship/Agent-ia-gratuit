cat > /root/ai_agents_project/src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Point d'entrée principal du système d'agents IA
"""

import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Ajouter le dossier src au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Routes de base
@app.route('/')
def index():
    return jsonify({
        "system": "AI Agents Platform",
        "version": "1.0.0",
        "endpoints": {
            "/api/status": "System status",
            "/api/agents": "List agents",
            "/api/docs": "Documentation"
        }
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "python_version": sys.version,
        "working_directory": os.getcwd(),
        "files_count": len(os.listdir('.')),
        "timestamp": os.times()
    })

@app.route('/api/agents')
def list_agents():
    agents = []
    for root_dir, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and ('agent' in file.lower() or 'ai' in file.lower()):
                agents.append({
                    "name": file,
                    "path": os.path.join(root_dir, file),
                    "size": os.path.getsize(os.path.join(root_dir, file))
                })
    return jsonify({
        "total_agents": len(agents),
        "agents": agents
    })

@app.route('/api/docs')
def documentation():
    return jsonify({
        "api": {
            "name": "AI Agents REST API",
            "description": "API for managing AI agents system",
            "version": "1.0.0"
        },
        "authentication": "API Key in header: X-API-Key",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "System overview"},
            {"path": "/api/status", "method": "GET", "description": "System status"},
            {"path": "/api/agents", "method": "GET", "description": "List all agents"},
            {"path": "/api/docs", "method": "GET", "description": "This documentation"}
        ]
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 AI AGENTS SYSTEM")
    print("=" * 50)
    print(f"Python: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Files found: {len(os.listdir('.'))}")
    print("\nStarting Flask server on http://0.0.0.0:5002")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
