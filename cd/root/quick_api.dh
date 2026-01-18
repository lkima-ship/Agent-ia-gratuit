# /root/quick_api.sh
#!/bin/bash
API_SCRIPT="/root/simple_working.py"

# Si pas d'argument, montrer l'aide
if [ $# -eq 0 ]; then
    echo "Usage:"
    echo "  $0 on     - Démarrer l'API"
    echo "  $0 off    - Arrêter l'API"
    echo "  $0 check  - Vérifier si l'API tourne"
    echo "  $0 test   - Tester l'endpoint /"
    exit 1
fi

case "$1" in
    on|start)
        echo "▶️  Démarrage..."
        pkill -f "$API_SCRIPT" 2>/dev/null
        nohup python3 "$API_SCRIPT" > /tmp/api.log 2>&1 &
        echo "✅ Démarré (port 5002)"
        ;;
    off|stop)
        echo "⏹️  Arrêt..."
        pkill -f "$API_SCRIPT" 2>/dev/null
        echo "✅ Arrêté"
        ;;
    check|status)
        if pgrep -f "$API_SCRIPT" > /dev/null; then
            echo "🟢 API en cours"
        else
            echo "🔴 API arrêtée"
        fi
        ;;
    test)
        timeout 2 curl -s http://localhost:5002 && echo "" || echo "❌ API non disponible"
        ;;
esac
