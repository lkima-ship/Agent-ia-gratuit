# 1. Arrêter tout
pkill -f python 2>/dev/null
rm -f /tmp/flask.pid /tmp/flask.log

# 2. CRÉER LA VERSION COMPLÈTE DE quick_api.sh
cat > /root/quick_api.sh << 'EOF'
#!/bin/sh

API_SCRIPT="/root/simple_working.py"
LOG_FILE="/tmp/flask.log"
PID_FILE="/tmp/flask.pid"

# Extraire le port du script Python
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
        FLASK_PID=$!
        echo $FLASK_PID > "$PID_FILE"
        
        echo "⏳ Attente du démarrage..."
        for i in $(seq 1 10); do
            if check_flask; then
                echo "✅ API démarrée avec succès!"
                echo "   PID: $FLASK_PID"
                echo "   Port: $PORT"
                exit 0
            fi
            sleep 0.5
        done
        
        echo "❌ L'API n'a pas démarré correctement"
        echo "📋 Logs:"
        tail -20 "$LOG_FILE"
        exit 1
        ;;
        
    off|stop)
        echo "🛑 Arrêt de l'API..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE" 2>/dev/null)
            if [ -n "$PID" ]; then
                kill $PID 2>/dev/null
                sleep 1
                kill -9 $PID 2>/dev/null 2>&1
            fi
        fi
        pkill -f "python3.*simple_working" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ API arrêtée"
        ;;
        
    check|status)
        echo "📊 Statut de l'API (port: $PORT):"
        if [ -f "$PID_FILE" ] && ps -p $(cat "$PID_FILE" 2>/dev/null) >/dev/null 2>&1; then
            PID=$(cat "$PID_FILE")
            echo "   Processus: 🟢 En cours (PID: $PID)"
            if check_flask; then
                echo "   Réponse HTTP: 🟢 OK"
                RESPONSE=$(curl -s --max-time 2 "http://localhost:$PORT")
                echo "   Message: $RESPONSE"
            else
                echo "   Réponse HTTP: 🔴 Échec"
            fi
        else
            echo "   Processus: 🔴 Arrêté"
        fi
        ;;
        
    test)
        echo "🧪 Test de l'API (port: $PORT)..."
        if check_flask; then
            echo "✅ Connecté avec succès!"
            RESPONSE=$(curl -s --max-time 3 "http://localhost:$PORT")
            echo "Réponse: $RESPONSE"
        else
            echo "❌ Échec de connexion"
        fi
        ;;
        
    logs)
        echo "📋 Journal de l'API:"
        if [ -f "$LOG_FILE" ]; then
            echo "Fichier: $LOG_FILE"
            echo "----------------------------------------"
            tail -50 "$LOG_FILE"
        else
            echo "Aucun fichier de log trouvé"
        fi
        ;;
        
    debug)
        echo "🐛 Mode debug - Exécution directe:"
        $0 off
        echo "Exécution de: python3 $API_SCRIPT"
        echo "----------------------------------------"
        cd /root
        python3 "$API_SCRIPT"
        ;;
        
    port)
        echo "🔌 Port configuré: $PORT"
        ;;
        
    help)
        echo "📚 Aide - Commandes disponibles:"
        echo "  api start    - Démarrer l'API"
        echo "  api stop     - Arrêter l'API"
        echo "  api status   - Vérifier l'état"
        echo "  api test     - Tester la connexion"
        echo "  api logs     - Afficher les logs"
        echo "  api debug    - Mode debug (premier plan)"
        echo "  api port     - Afficher le port configuré"
        echo "  api help     - Cette aide"
        echo ""
        echo "Alias: on, off, check pour start, stop, status"
        echo ""
        echo "⚠️  Port actuel: $PORT"
        ;;
        
    *)
        echo "❌ Commande inconnue: $1"
        echo "Utilisez 'api help' pour voir les commandes disponibles"
        exit 1
        ;;
esac
EOF

# 3. RENDRE EXÉCUTABLE
chmod +x /root/quick_api.sh

# 4. RECRÉER LE LIEN SYMBOLIQUE
rm -f /usr/local/bin/api
ln -sf /root/quick_api.sh /usr/local/bin/api

# 5. VÉRIFIER QUE LE SCRIPT FLASK UTILISE LE PORT 5002
sed -i "s/port=[0-9]*/port=5002/" /root/simple_working.py

# 6. TESTER
echo "=== TEST COMPLET ==="
api help
echo ""
api start
echo ""
api status
echo ""
api test
echo ""
api port
