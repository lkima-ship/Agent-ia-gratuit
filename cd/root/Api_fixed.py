cat > /root/api_fixed.py << 'EOF'
#!/usr/bin/env python3
"""
API REST Agents IA - Version corrigée
"""

from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "system": "AI Agents Platform",
        "version": "2.0",
        "status": "online",
        "endpoints": [
            "/api/agents",
            "/api/status",
            "/api/system"
        ]
    })

@app.route('/api/agents')
def list_agents():
    agents = []
    for filename in os.listdir('/root'):
        if filename.endswith('.py'):
            if 'agent' in filename.lower() or 'ia' in filename.lower():
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
        "timestamp": time.time(),
        "time": time.ctime(),
        "python_version": os.popen('python3 --version').read().strip()
    })

@app.route('/api/system')
def system_info():
    import psutil
    return jsonify({
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 API REST Agents IA - Version corrigée")
    print("🌐 URL: http://0.0.0.0:5002")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
