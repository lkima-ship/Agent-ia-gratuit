# Créez une API améliorée
cat > /root/api_agents_complete.py << 'EOF'
from flask import Flask, jsonify
import os
import time
import sys

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "system": "AI Agents Platform",
        "version": "2.0",
        "status": "online",
        "timestamp": time.time(),
        "endpoints": [
            "/api/agents",
            "/api/status",
            "/api/system",
            "/api/docs"
        ]
    })

@app.route('/api/agents')
def list_agents():
    agents = []
    for filename in os.listdir('/root'):
        if filename.endswith('.py') and ('agent' in filename.lower() or 'ia' in filename.lower()):
            try:
                size = os.path.getsize(f"/root/{filename}")
                agents.append({
                    "name": filename,
                    "size": size,
                    "type": "python"
                })
            except:
                continue
    
    return jsonify({
        "total": len(agents),
        "agents": agents
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "time": time.ctime(),
        "python_version": sys.version.split()[0],
        "hostname": os.uname().nodename,
        "files_count": len(os.listdir('/root'))
    })

@app.route('/api/system')
def system_info():
    try:
        import psutil
        return jsonify({
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent
        })
    except:
        return jsonify({
            "message": "Install psutil for system info"
        })

@app.route('/api/docs')
def documentation():
    return jsonify({
        "API": "AI Agents REST API",
        "description": "API for managing AI agents",
        "usage": {
            "list_agents": "GET /api/agents",
            "system_status": "GET /api/status",
            "system_info": "GET /api/system",
            "documentation": "GET /api/docs"
        }
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 AI AGENTS API - COMPLETE VERSION")
    print("🌐 http://0.0.0.0:5002")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
