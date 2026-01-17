cat > /root/start_main_agents.sh << 'EOF'
#!/bin/sh
echo "Démarrage des agents principaux..."
echo ""

# Fonction pour démarrer un agent
start_agent() {
    if [ -f "$1" ]; then
        echo "Démarrage: $(basename $1)"
        nohup python3 "$1" > "/tmp/$(basename $1).log" 2>&1 &
        echo "  PID: $! | Log: /tmp/$(basename $1).log"
    else
        echo "Erreur: $1 non trouvé"
    fi
}

# Démarrer les agents disponibles
if [ -f "/root/hub_agents.py" ]; then
    start_agent "/root/hub_agents.py"
fi

if [ -f "/root/dashboard_web_agent.py" ]; then
    start_agent "/root/dashboard_web_agent.py"
fi

if [ -f "/root/interface_agents_web.py" ]; then
    start_agent "/root/interface_agents_web.py"
fi

echo ""
echo "Vérification des processus..."
ps aux | grep python | grep -v grep
echo ""
echo "Utilisez: tail -f /tmp/*.log pour voir les logs"
EOF

chmod +x /root/start_main_agents.sh
