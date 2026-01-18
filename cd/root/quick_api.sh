# Recréer quick_api.sh avec plus de robustesse
cat > /root/quick_api.sh << 'EOF'
#!/bin/sh
API_SCRIPT="/root/simple_working.py"
LOG_FILE="/tmp/flask.log"

case "$1" in
    on|start)
        echo "▶️  Démarrage de l'API Flask..."
        # Arrêter proprement
        pkill -f "python3.*simple_working" 2>/dev/null
        sleep 1
        
        # Démarrer avec nohup et redirection
        nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
        PID=$!
        echo $PID > /tmp/flask.pid
        
        # Attendre un peu pour le démarrage
        echo "Attente du démarrage (3s)..."
        sleep 3
        
        # Vérifier si le processus tourne toujours
        if kill -0 $PID 2>/dev/null; then
            echo "✅ API démarrée (PID: $PID, Port: 5002)"
            echo "Logs: $LOG_FILE"
        else
            echo "❌ Échec du démarrage. Voir logs:"
            tail -20 "$LOG_FILE"
        fi
        ;;
        
    off|stop)
        echo "⏹️  Arrêt de l'API..."
        if [ -f /tmp/flask.pid ]; then
            PID=$(cat /tmp/flask.pid)
            kill $PID 2>/dev/null
            sleep 1
        fi
        pkill -f "python3.*simple_working" 2>/dev/null
        rm -f /tmp/flask.pid
        echo "✅ API arrêtée"
        ;;
        
    check|status)
        if [ -f /tmp/flask.pid ] && kill -0 $(cat /tmp/flask.pid) 2>/dev/null; then
            echo "🟢 API en cours (PID: $(cat /tmp/flask.pid))"
            
            # Tester la connexion
            if curl -s --connect-timeout 2 http://localhost:5002 >/dev/null; then
                echo "   ✅ Endpoint / accessible"
            else
                echo "   ⚠️  Endpoint / non accessible"
            fi
        else
            echo "🔴 API arrêtée"
            # Nettoyer le pid fichier s'il existe
            rm -f /tmp/flask.pid
        fi
        ;;
        
    test)
        echo "🧪 Test de l'API..."
        if curl -s --max-time 5 http://localhost:5002; then
            echo ""
        else
            echo "❌ Aucune réponse de l'API"
        fi
        ;;
        
    logs)
        if [ -f "$LOG_FILE" ]; then
            tail -50 "$LOG_FILE"
        else
            echo "Aucun fichier de log trouvé"
        fi
        ;;
        
    restart)
        echo "🔄 Redémarrage..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart|status|test|logs}"
        echo "Alias: on, off, check"
        exit 1
        ;;
esac
EOF

# Rendre exécutable
chmod +x /root/quick_api.sh

# Recréer le lien
rm -f /usr/local/bin/api
ln -sf /root/quick_api.sh /usr/local/bin/api
