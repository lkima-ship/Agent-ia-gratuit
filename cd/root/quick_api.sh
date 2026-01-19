# Télécharger/écrire la version complète
cat > /root/quick_api.sh << 'EOF'
#!/bin/sh

API_SCRIPT="/root/simple_working.py"
LOG_FILE="/tmp/flask.log"
PID_FILE="/tmp/flask.pid"

# Fonction pour extraire le port du script
get_port() {
    PORT=$(grep -o "port=[0-9]*" "$API_SCRIPT" 2>/dev/null | head -1 | cut -d= -f2)
    if [ -z "$PORT" ]; then
        PORT=5002
    fi
    echo $PORT
}

PORT=$(get_port)

# Vérifier si Flask répond
check_flask() {
    curl -s --max-time 2 "http://localhost:$PORT" >/dev/null 2>&1
    return $?
}

case "$1" in
    on|start)
        echo "🚀 Démarrage de l'API Flask (port: $PORT)..."
        $0 off >/dev/null 2>&1
        sleep 1
        cd /root
        nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
        for i in $(seq 1 10); do
            if check_flask; then
                echo "✅ API démarrée (PID: $(cat $PID_FILE))"
                exit 0
            fi
            sleep 0.5
        done
        echo "❌ Échec du démarrage"
        tail -20 "$LOG_FILE"
        exit 1
        ;;
        
    off|stop)
        echo "🛑 Arrêt de l'API..."
        if [ -f "$PID_FILE" ]; then
            kill $(cat "$PID_FILE") 2>/dev/null
            sleep 1
        fi
        pkill -f "python3.*simple_working" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ API arrêtée"
        ;;
        
    check|status)
        echo "📊 Statut de l'API:"
        if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE") >/dev/null 2>&1; then
            echo "   Processus: 🟢 En cours (PID: $(cat $PID_FILE))"
            if check_flask; then
                echo "   HTTP: 🟢 OK"
                echo "   Réponse: $(curl -s http://localhost:$PORT)"
            else
                echo "   HTTP: 🔴 Échec"
            fi
        else
            echo "   Processus: 🔴 Arrêté"
        fi
        echo "   Port: $PORT"
        ;;
        
    test)
        echo "🧪 Test de l'API (port: $PORT)..."
        if check_flask; then
            echo "✅ Connecté!"
            curl -s "http://localhost:$PORT"
            echo ""
        else
            echo "❌ Échec"
        fi
        ;;
        
    logs)
        echo "📋 Journal de l'API:"
        if [ -f "$LOG_FILE" ]; then
            tail -50 "$LOG_FILE"
        else
            echo "Aucun fichier de log"
        fi
        ;;
        
    debug)
        echo "🐛 Mode debug:"
        $0 off
        cd /root
        python3 "$API_SCRIPT"
        ;;
        
    port)
        echo "🔌 Port configuré: $PORT"
        ;;
        
    help)
        echo "📚 Commandes:"
        echo "  api start    - Démarrer"
        echo "  api stop     - Arrêter"
        echo "  api status   - Vérifier"
        echo "  api test     - Tester"
        echo "  api logs     - Logs"
        echo "  api debug    - Mode debug"
        echo "  api port     - Afficher port"
        echo "  api help     - Aide"
        echo ""
        echo "Alias: on, off, check"
        ;;
        
    *)
        echo "❌ Commande inconnue"
        echo "Utilisez: api help"
        exit 1
        ;;
esac
EOF

# Rendre exécutable
chmod +x /root/quick_api.sh
