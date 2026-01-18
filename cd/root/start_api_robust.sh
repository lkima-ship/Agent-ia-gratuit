cat > /root/start_api_robust.sh << 'EOF'
#!/bin/sh

echo "🚀 Démarrage API robuste..."

# Arrêter toute API existante
pkill -f "python.*:5002" 2>/dev/null
sleep 3

# Vérifier les dépendances
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installation de Flask..."
    pip3 install flask
fi

if ! python3 -c "import psutil" 2>/dev/null; then
    echo "Installation de psutil..."
    pip3 install psutil
fi

# Démarrer
cd /root
python3 api_fixed.py > /var/log/ai_api.log 2>&1 &
API_PID=$!

echo "Attente du démarrage..."
for i in 1 2 3 4 5 6 7 8 9 10; do
    if curl -s http://localhost:5002 > /dev/null 2>&1; then
        echo "✅ API prête après ${i} secondes"
        echo "PID: $API_PID"
        echo "Logs: /var/log/ai_api.log"
        echo "URL: http://localhost:5002"
        
        # Test automatique
        echo -e "\n📊 Test automatique:"
        curl -s "http://localhost:5002/api/agents" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    print(f'Agents: {data[\"total\"]}')
except:
    print('Test échoué')
"
        exit 0
    fi
    sleep 1
done

echo "❌ Échec du démarrage après 10 secondes"
echo "Dernières lignes du log:"
tail -20 /var/log/ai_api.log
exit 1
EOF

chmod +x /root/start_api_robust.sh
