cat > /root/start_final.sh << 'EOF'
#!/bin/sh

echo "=== DÉMARRAGE API AGENTS IA ==="

# Arrêter les APIs existantes
pkill -f "python.*:500[0-9]" 2>/dev/null
sleep 2

# Vérifier Flask
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installation de Flask..."
    pip3 install flask
fi

# Démarrer l'API sur le port 5002
echo "Port 5002..."
cd /root
python3 -c "
from flask import Flask, jsonify
import os
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'system': 'AI Agents',
        'status': 'online',
        'files': len(os.listdir('.')),
        'agents': [f for f in os.listdir('.') if 'agent' in f]
    })

@app.route('/api/ping')
def ping():
    return jsonify({'ping': 'pong'})

if __name__ == '__main__':
    print('🚀 API démarrée: http://0.0.0.0:5002')
    print('📁 Agents détectés:', len([f for f in os.listdir('.') if 'agent' in f]))
    app.run(host='0.0.0.0', port=5002, debug=False)
" > /tmp/api_output.log 2>&1 &
API_PID=$!

echo "PID: $API_PID"
echo "Attente du démarrage..."

# Attendre avec vérification
for i in 1 2 3 4 5; do
    echo -n "."
    sleep 1
    if curl -s http://localhost:5002 > /dev/null 2>&1; then
        echo -e "\n✅ API PRÊTE!"
        break
    fi
done

echo -e "\n=== TEST ==="
curl -s http://localhost:5002 || echo "Échec, vérifiez: tail -f /tmp/api_output.log"
EOF

chmod +x /root/start_final.sh
