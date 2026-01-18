cat > /root/api_manager.sh << 'EOF'
#!/bin/sh

case "$1" in
    start)
        # Arrêter d'abord si déjà en cours
        pkill -f "python.*:5002" 2>/dev/null
        sleep 2
        
        echo "🤖 Démarrage API Agents IA..."
        cd /root
        python3 -c "
from flask import Flask, jsonify
import os, time

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'system': 'AI Agents Platform',
        'version': '1.0',
        'status': 'online',
        'endpoints': ['/api/agents', '/api/status', '/api/docs']
    })

@app.route('/api/agents')
def agents():
    agents_list = []
    for f in os.listdir('.'):
        if f.endswith('.py') and ('agent' in f.lower() or 'ia' in f.lower()):
            agents_list.append(f)
    return jsonify({
        'total': len(agents_list),
        'agents': agents_list
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'time': time.ctime(),
        'directory': os.getcwd(),
        'python_version': os.popen('python3 --version').read().strip()
    })

@app.route('/api/docs')
def docs():
    return jsonify({
        'api': 'AI Agents REST API',
        'usage': 'Use endpoints below',
        'endpoints': {
            '/': 'System overview',
            '/api/agents': 'List all AI agents',
            '/api/status': 'System status',
            '/api/docs': 'This documentation'
        }
    })

if __name__ == '__main__':
    print('=' * 50)
    print('🤖 AI AGENTS API - Port 5002')
    print('🌐 http://localhost:5002')
    print('=' * 50)
    app.run(host='0.0.0.0', port=5002, debug=False)
" > /var/log/ai_api.log 2>&1 &
        
        API_PID=$!
        echo $API_PID > /tmp/ai_api.pid
        
        sleep 3
        if curl -s http://localhost:5002 > /dev/null; then
            echo "✅ API démarrée (PID: $API_PID)"
            echo "📊 Test: curl http://localhost:5002/api/agents"
        else
            echo "❌ Échec, voir: tail -f /var/log/ai_api.log"
        fi
        ;;
    
    stop)
        echo "🛑 Arrêt de l'API..."
        pkill -f "python.*:5002"
        sleep 2
        echo "✅ API arrêtée"
        ;;
    
    status)
        echo "🔍 État de l'API:"
        if curl -s http://localhost:5002/api/status > /dev/null; then
            echo "✅ EN LIGNE"
            curl -s http://localhost:5002/api/status | python3 -m json.tool
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
        echo "📝 Logs API:"
        tail -20 /var/log/ai_api.log 2>/dev/null || echo "Aucun log trouvé"
        ;;
    
    *)
        echo "Usage: $0 {start|stop|status|restart|logs}"
        echo ""
        echo "🤖 Gestion API Agents IA"
        echo "  start    - Démarrer l'API sur le port 5002"
        echo "  stop     - Arrêter l'API"
        echo "  status   - Vérifier l'état"
        echo "  restart  - Redémarrer"
        echo "  logs     - Afficher les logs"
        exit 1
        ;;
esac
EOF

chmod +x /root/api_manager.sh
