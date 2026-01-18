cat > /root/api_smart_start.sh << 'EOF'
#!/bin/sh

echo "🤖 Démarrage intelligent de l'API..."

# Nettoyer
rm -f /tmp/api_running 2>/dev/null

# Démarrer l'API avec un indicateur de démarrage
cd /root
python3 -c "
import time
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'service': 'AI Agents API',
        'status': 'online',
        'timestamp': time.time()
    })

@app.route('/api/ready')
def ready():
    return jsonify({'ready': True})

@app.route('/api/agents')
def agents():
    agents = [f for f in os.listdir('.') if 'agent' in f.lower() and f.endswith('.py')]
    return jsonify({'total': len(agents), 'agents': agents[:10]})

if __name__ == '__main__':
    # Créer un fichier pour indiquer que l'API a démarré
    with open('/tmp/api_running', 'w') as f:
        f.write('starting')
    
    print('=' * 50)
    print('🚀 API Agents IA - Démarrage')
    print('📡 Attendez les messages Flask ci-dessous...')
    print('=' * 50)
    
    app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)
" > /tmp/api_smart.log 2>&1 &
PID=$!

echo "Processus lancé avec PID: $PID"
echo "En attente des signaux de démarrage..."

# Attendre les messages Flask
timeout=15
for i in $(seq 1 $timeout); do
    # Vérifier si le processus est toujours en vie
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "❌ Le processus s'est arrêté prématurément"
        echo "Logs:"
        tail -20 /tmp/api_smart.log
        exit 1
    fi
    
    # Vérifier dans les logs si Flask a démarré
    if grep -q "Running on" /tmp/api_smart.log 2>/dev/null; then
        echo "✅ Flask a signalé le démarrage"
        sleep 1  # Donner un peu plus de temps
        break
    fi
    
    # Vérifier si on peut se connecter
    if curl -s http://localhost:5002/api/ready > /dev/null 2>&1; then
        echo "✅ API accessible (test direct)"
        break
    fi
    
    echo -n "."
    sleep 1
done

# Test final
echo -e "\n🎯 Test final de connexion..."
if curl -s http://localhost:5002/api/ready > /dev/null; then
    echo "========================================"
    echo "🎉 API DÉMARRÉE AVEC SUCCÈS !"
    echo "🌐 URL: http://localhost:5002"
    echo "📊 Test: curl http://localhost:5002/api/agents"
    echo "========================================"
    
    # Afficher un exemple
    curl -s "http://localhost:5002/api/agents" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'📁 {data[\"total\"]} agents détectés')
except:
    print('⚠️  Problème de récupération')
"
else
    echo "❌ Échec - L'API n'est pas accessible après $timeout secondes"
    echo "Derniers logs:"
    tail -20 /tmp/api_smart.log
    echo "Arrêt du processus..."
    kill $PID 2>/dev/null
fi
EOF

chmod +x /root/api_smart_start.sh
