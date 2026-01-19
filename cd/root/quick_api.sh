# Créer une version améliorée qui détecte le port automatiquement
cat > /root/quick_api.sh << 'EOF'
#!/bin/sh

API_SCRIPT="/root/simple_working.py"
LOG_FILE="/tmp/flask.log"
PID_FILE="/tmp/flask.pid"

# Fonction pour extraire le port du script Python
get_port() {
    # Chercher le port dans le script
    PORT=$(grep -o "port=[0-9]*" "$API_SCRIPT" | head -1 | cut -d= -f2)
    if [ -z "$PORT" ]; then
        PORT=5002  # Port par défaut
    fi
    echo $PORT
}

PORT=$(get_port)

# Fonction pour vérifier si Flask répond
check_flask() {
    curl -s --max-time 2 "http://localhost:$PORT" >/dev/null 2>&1
    return $?
}

case "$1" in
    on|start)
        echo "🚀 Démarrage de l'API Flask (port: $PORT)..."
        
        # Arrêter d'abord
        $0 off >/dev/null 2>&1
        sleep 1
        
        # Vérifier si le script existe
        if [ ! -f "$API_SCRIPT" ]; then
            echo "❌ Erreur: $API_SCRIPT n'existe pas"
            exit 1
        fi
        
        # Démarrer
        cd /root
        nohup python3 "$API_SCRIPT" > "$LOG_FILE" 2>&1 &
        FLASK_PID=$!
        echo $FLASK_PID > "$PID_FILE"
        
        echo "⏳ Attente du démarrage..."
        
        # Attendre et vérifier
        for i in $(seq 1 10); do
            if check_flask; then
                echo "✅ API démarrée avec succès!"
                echo "   PID: $FLASK_PID"
                echo "   Port: $PORT"
                echo "   Test: curl http://localhost:$PORT"
                exit 0
            fi
            sleep 0.5
        done
        
        # Si on arrive ici, l'API n'a pas démarré
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
        pkill -f "python.*simple_working" 2>/dev/null
        rm -f "$PID_FILE"
        echo "✅ API arrêtée"
        ;;
        
    check|status)
        echo "📊 Statut de l'API (port: $PORT):"
        
        # Vérifier le processus
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE" 2>/dev/null)
            if [ -n "$PID" ] && ps -p $PID >/dev/null 2>&1; then
                echo "   Processus: 🟢 En cours (PID: $PID)"
                
                # Vérifier la réponse HTTP
                if check_flask; then
                    echo "   Réponse HTTP: 🟢 OK"
                    echo "   Message: $(curl -s --max-time 2 http://localhost:$PORT)"
                else
                    echo "   Réponse HTTP: 🔴 Échec"
                fi
            else
                echo "   Processus: 🔴 Arrêté"
                rm -f "$PID_FILE"
            fi
        else
            echo "   Processus: 🔴 Jamais démarré"
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
            echo "Vérifiez:"
            echo "   1. L'API est-elle démarrée? (api status)"
            echo "   2. Le port $PORT est-il libre?"
            echo "   3. Y a-t-il des erreurs? (api logs)"
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
        echo "🐛 Mode debug - Exécution directe (port: $PORT):"
        $0 off
        echo "Exécution de: python3 $API_SCRIPT"
        echo "----------------------------------------"
        cd /root
        python3 "$API_SCRIPT"
        ;;
        
    port)
        echo "🔌 Port configuré: $PORT"
        echo "Pour changer: éditez 'port=...' dans $API_SCRIPT"
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

# Rendre exécutable
chmod +x /root/quick_api.sh

# Recréer le lien
ln -sf /root/quick_api.sh /usr/local/bin/api
