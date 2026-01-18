cat > /root/launch_api.sh << 'EOF'
#!/bin/sh

# Arrêter toute API existante
echo "🛑 Arrêt des processus existants..."
pkill -f "python.*:5002" 2>/dev/null
pkill -f "flask" 2>/dev/null
sleep 3

# Vérifier Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installation de Flask..."
    pip3 install flask 2>/dev/null || {
        echo "⚠️ Échec installation Flask"
    }
fi

# Créer un script Python minimal et sûr
cat > /root/api_minimal_safe.py << 'PYEOF'
from flask import Flask, jsonify
import os
import time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"status": "online", "service": "AI Agents", "time": time.ctime()})

@app.route('/api/agents')
def agents():
    files = os.listdir('/root')
    agents = [f for f in files if f.endswith('.py') and ('agent' in f.lower() or 'ia' in f.lower())]
    return jsonify({"total": len(agents), "agents": agents})

if __name__ == '__main__':
    print("Server starting on http://0.0.0.0:5002")
    app.run(host='0.0.0.0', port=5002, debug=False)
PYEOF

# Démarrer
echo "🚀 Démarrage de l'API..."
cd /root
python3 api_minimal_safe.py > /var/log/api_safe.log 2>&1 &
PID=$!

echo "PID: $PID"
echo "Attente 8 secondes..."

# Attendre avec vérification
for i in $(seq 1 8); do
    sleep 1
    if curl -s http://localhost:5002 > /dev/null 2>&1; then
        echo "✅ API prête après $i secondes!"
        
        # Afficher un test
        echo -e "\n📊 Test automatique:"
        curl -s "http://localhost:5002/api/agents" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'   Agents: {data[\"total\"]}')
    if data['total'] > 0:
        print('   Exemples:')
        for agent in data['agents'][:3]:
            print(f'     • {agent}')
except:
    print('   Test échoué')
"
        echo -e "\n🔗 URL: http://localhost:5002"
        echo "📝 Logs: /var/log/api_safe.log"
        exit 0
    fi
done

echo "❌ Échec après 8 secondes"
echo "Logs:"
tail -20 /var/log/api_safe.log
exit 1
EOF

chmod +x /root/launch_api.sh
