cat > /root/manage_api.sh << 'EOF'
#!/bin/sh

API_PID_FILE="/tmp/api_agents.pid"
API_LOG="/tmp/api_agents.log"

case "$1" in
    start)
        echo "🚀 Démarrage API Agents IA..."
        
        # Arrêter si déjà en cours
        if [ -f "$API_PID_FILE" ]; then
            kill $(cat "$API_PID_FILE") 2>/dev/null
            sleep 2
        fi
        
        # Démarrer l'API simple
        cd /root
        python3 -c "
from flask import Flask, jsonify
import os, time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'service': 'AI Agents API',
        'status': 'online',
        'timestamp': time.time()
    })

@app.route('/api/agents')
def agents():
    agents = []
    for f in os.listdir('.'):
        if f.endswith('.py') and ('agent' in f.lower() or 'ia' in f.lower()):
            agents.append(f)
    return jsonify({'total': len(agents), 'agents': agents})

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'time': time.ctime(),
        'directory': os.getcwd()
    })

@app.route('/api/ping')
def ping():
    return jsonify({'ping': 'pong'})

print('Starting API on http://0.0.0.0:5002')
app.run(host='0.0.0.0', port=5002, debug=False, use_reloader=False)
" > "$API_LOG" 2>&1 &
        
        API_PID=$!
        echo $API_PID > "$API_PID_FILE"
        
        echo "PID: $API_PID"
        echo "Attente 5 secondes..."
        
        # Attendre et vérifier
        for i in {1..10}; do
            sleep 1
            if curl -s http://localhost:5002/api/ping > /dev/null 2>&1; then
                echo "✅ API démarrée avec succès!"
                echo "📡 URL: http://localhost:5002"
                echo "📝 Logs: $API_LOG"
                exit 0
            fi
        done
        
        echo "❌ Échec du démarrage"
        echo "Dernières lignes du log:"
        tail -10 "$API_LOG"
        ;;
    
    stop)
        echo "🛑 Arrêt de l'API..."
        if [ -f "$API_PID_FILE" ]; then
            kill $(cat "$API_PID_FILE") 2>/dev/null
            rm -f "$API_PID_FILE"
            echo "✅ API arrêtée"
        else
            echo "⚠️ Aucun PID trouvé, arrêt des processus Python sur le port 5002"
            pkill -f "python.*:5002" 2>/dev/null
        fi
        sleep 2
        ;;
    
    status)
        echo "🔍 État de l'API:"
        if curl -s http://localhost:5002/api/ping > /dev/null 2>&1; then
            echo "✅ EN LIGNE"
            echo "Test rapide:"
            curl -s http://localhost:5002/api/ping | python3 -m json.tool 2>/dev/null
        else
            echo "❌ HORS LIGNE"
            echo "Processus:"
            ps aux | grep -E "python.*:5002" | grep -v grep || echo "Aucun processus"
        fi
        ;;
    
    restart)
        echo "🔄 Redémarrage..."
        $0 stop
        sleep 2
        $0 start
        ;;
    
    logs)
        echo "📝 Logs de l'API:"
        if [ -f "$API_LOG" ]; then
            tail -20 "$API_LOG"
        else
            echo "Aucun log trouvé"
        fi
        ;;
    
    *)
        echo "Usage: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "🤖 Gestionnaire API Agents IA"
        echo "  start    - Démarrer l'API sur le port 5002"
        echo "  stop     - Arrêter l'API"
        echo "  status   - Vérifier l'état de l'API"
        echo "  restart  - Redémarrer l'API"
        echo "  logs     - Afficher les logs"
        ;;
esac
EOF

chmod +x /root/manage_api.sh
