# Mettre à jour quick_api.sh avec plus de débogage
cat > /root/quick_api.sh << 'EOF'
#!/bin/sh

API_SCRIPT="/root/simple_working.py"
LOG_FILE="/tmp/flask.log"
PID_FILE="/tmp/flask.pid"

# Fonction pour vérifier si le port est en écoute
check_port() {
    netstat -tlnp 2>/dev/null | grep :5002 >/dev/null
    return $?
}

# Fonction pour vérifier si Flask répond
check_flask() {
    curl -s --max-time 2 http://localhost:5002 >/dev/null 2>&1
    return $?
}

case "$1" in
    on|start)
        echo "🚀 Démarrage de l'API Flask..."
        
        # Arrêter d'abord
        $0 stop 2>/dev/null
        
        # Démarrer
        cd /root
        nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
        FLASK_PID=$!
        echo $FLASK_PID > "$PID_FILE"
        
        echo "Attente du démarrage (5 secondes)..."
        for i in $(seq 1 10); do
            if check_flask; then
                echo "✅ API démarrée avec succès (PID: $FLASK_PID)"
                echo "📝 Logs: $LOG_FILE"
                echo "🌐 Test: curl http://localhost:5002"
                exit 0
            fi
            sleep 0.5
        done
        
        # Si on arrive ici, l'API n'a pas démarré
        echo "❌ L'API n'a pas démarré. Vérifiez les logs:"
        tail -20 "$LOG_FILE"
        exit 1
        ;;
        
    off|stop)
        echo "🛑 Arrêt de l'API..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            kill $PID 2>/dev/null
            sleep 1
            kill -9 $PID 2>/dev/null 2>&1
        fi
        pkill -f "python3.*simple_working" 2>/dev/null
        pkill -f "python.*simple_working" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ API arrêtée"
        ;;
        
    check|status)
        if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") >/dev/null 2>&1; then
            PID=$(cat "$PID_FILE")
            if check_flask; then
                echo "🟢 API en cours (PID: $PID) - Répond correctement"
            else
                echo "🟡 API en cours (PID: $PID) mais ne répond pas au test"
            fi
        else
            echo "🔴 API arrêtée"
        fi
        ;;
        
    test)
        echo "🧪 Test de connexion à l'API..."
        if check_flask; then
            echo "✅ Connecté à l'API"
            curl -s http://localhost:5002
            echo ""
        else
            echo "❌ Impossible de se connecter à l'API"
        fi
        ;;
        
    logs)
        if [ -f "$LOG_FILE" ]; then
            echo "📋 Dernières lignes des logs:"
            echo "----------------------------"
            tail -30 "$LOG_FILE"
        else
            echo "Aucun fichier de log trouvé"
        fi
        ;;
        
    debug)
        echo "🐛 Mode debug - Exécution en premier plan:"
        $0 stop
        cd /root
        python3 "$API_SCRIPT"
        ;;
        
    *)
        echo "Usage: $0 {start|stop|status|test|logs|debug}"
        echo "  start  - Démarrer l'API"
        echo "  stop   - Arrêter l'API"
        echo "  status - Vérifier l'état"
        echo "  test   - Tester la connexion"
        echo "  logs   - Afficher les logs"
        echo "  debug  - Exécuter en mode debug (premier plan)"
        exit 1
        ;;
esac
EOF

# Rendre exécutable
chmod +x /root/quick_api.sh

# Recréer le lien
ln -sf /root/quick_api.sh /usr/local/bin/api
