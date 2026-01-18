cat > /root/api_correct.py << 'EOF'
#!/usr/bin/env python3
"""
API REST Agents IA - Version sans erreurs
"""

from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "system": "AI Agents Platform",
        "version": "1.0",
        "status": "online",
        "port": 5002,
        "timestamp": time.time()
    })

@app.route('/api/agents')
def agents():
    agents_list = []
    for filename in os.listdir('/root'):
        if filename.endswith('.py') and ('agent' in filename.lower() or 'ia' in filename.lower()):
            agents_list.append(filename)
    
    return jsonify({
        "total": len(agents_list),
        "agents": agents_list[:20]  # Limiter à 20 pour l'affichage
    })

@app.route('/api/status')
def status():
    return jsonify({
        "status": "online",
        "time": time.ctime(),
        "python_version": os.popen('python3 --version').read().strip(),
        "files_in_root": len(os.listdir('/root'))
    })

if __name__ == '__main__':
    print("=" * 50)
    print("🤖 API REST Agents IA")
    print("🌐 http://0.0.0.0:5002")
    print("📁 Dossier: /root")
    print("=" * 50)
    app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)
EOF
