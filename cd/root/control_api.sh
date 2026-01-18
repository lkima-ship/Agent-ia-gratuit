# /root/control_api.sh
#!/bin/bash

case "$1" in
    start)
        echo "Démarrage de l'API..."
        pkill -f python 2>/dev/null
        python3 /root/simple_working.py 2>&1 | tee /tmp/flask_output.log &
        echo $! > /tmp/flask.pid
        sleep 3
        echo "API démarrée sur http://localhost:5002"
        ;;
    stop)
        echo "Arrêt de l'API..."
        pkill -f python 2>/dev/null
        rm -f /tmp/flask.pid
        echo "API arrêtée"
        ;;
    status)
        if pgrep -f "simple_working.py" > /dev/null; then
            echo "✅ API en cours d'exécution (PID: $(cat /tmp/flask.pid 2>/dev/null))"
            echo "Log: /tmp/flask_output.log"
        else
            echo "❌ API arrêtée"
        fi
        ;;
    restart)
        $0 stop
        sleep 2
        $0 start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        ;;
esac
