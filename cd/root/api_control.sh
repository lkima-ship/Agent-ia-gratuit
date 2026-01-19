# Créer une version simplifiée mais complète
cat > /root/api_control.sh << 'EOF'
#!/bin/sh
case "$1" in
    start|on)
        echo "Démarrage API..."
        pkill -f python 2>/dev/null
        cd /root
        nohup python3 simple_working.py > /tmp/api.log 2>&1 &
        echo $! > /tmp/api.pid
        sleep 2
        echo "✅ API démarrée sur http://localhost:5002"
        ;;
    stop|off)
        echo "Arrêt API..."
        pkill -f python 2>/dev/null
        rm -f /tmp/api.pid
        echo "✅ API arrêtée"
        ;;
    status|check)
        if ps aux | grep -v grep | grep "simple_working.py" >/dev/null; then
            echo "🟢 API en cours (PID: $(cat /tmp/api.pid 2>/dev/null))"
            # Tester la connexion
            if curl -s --max-time 2 http://localhost:5002 >/dev/null; then
                echo "   ✅ Répond correctement"
            else
                echo "   ⚠️  Tourne mais ne répond pas"
            fi
        else
            echo "🔴 API arrêtée"
        fi
        ;;
    test)
        echo "Test de l'API..."
        curl -s http://localhost:5002 && echo "" || echo "❌ Pas de réponse"
        ;;
    logs)
        tail -20 /tmp/api.log 2>/dev/null || echo "Pas de logs"
        ;;
    *)
        echo "Usage: $0 {start|stop|status|test|logs}"
        echo "Alias: on, off, check"
        ;;
esac
EOF

# Rendre exécutable
chmod +x /root/api_control.sh

# Créer un lien symbolique
ln -sf /root/api_control.sh /usr/local/bin/api
