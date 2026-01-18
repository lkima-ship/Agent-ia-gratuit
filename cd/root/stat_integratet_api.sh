cat > /root/start_integrated_api.sh << 'EOF'
#!/bin/bash

echo "🚀 Démarrage du système intégré API + Agents IA"

# Arrêter l'API précédente si elle existe
pkill -f "api_rest" 2>/dev/null
sleep 2

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import flask, flask_cors" 2>/dev/null || {
    echo "Installation de Flask..."
    pip3 install flask flask-cors
}

# Démarrer l'API adaptée
echo "🌐 Démarrage de l'API REST sur le port 5002..."
cd /root
python3 api_rest_agents.py > /var/log/ia_api.log 2>&1 &
API_PID=$!
echo $API_PID > /tmp/ia_api.pid

# Attendre et vérifier
sleep 3
if curl -s http://localhost:5002/api/agents > /dev/null; then
    echo "✅ API démarrée avec succès (PID: $API_PID)"
    
    # Afficher le résumé
    echo ""
    echo "📊 RÉSUMÉ DU SYSTÈME:"
    curl -s http://localhost:5002/api/system/status | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Agents installés: {data[\"agents_installed\"]}')
print(f'Mémoire: {data[\"memory_usage\"]}')
print(f'Disque: {data[\"disk_usage\"]}')
"
    
    echo ""
    echo "🔗 ACCÈS:"
    echo "API: http://localhost:5002/api/agents"
    echo "Docs: http://localhost:5002/api/docs"
    echo "Logs: /var/log/ia_api.log"
    
else
    echo "❌ Échec du démarrage de l'API"
    tail -20 /var/log/ia_api.log
fi
EOF

chmod +x /root/start_integrated_api.sh
