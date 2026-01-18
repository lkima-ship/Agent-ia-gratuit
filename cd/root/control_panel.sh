cat > /root/control_panel.sh << 'EOF'
#!/bin/bash

# Menu de contrôle pour le système d'agents IA
BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

check_status() {
    echo -e "\n${BLUE}=== ÉTAT DU SYSTÈME ===${NC}"
    
    # Vérifier API REST
    if curl -s http://localhost:5002/api/agents > /dev/null 2>&1; then
        echo -e "API REST: ${GREEN}✅ EN LIGNE (port 5002)${NC}"
        curl -s http://localhost:5002/api/system/status | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(f'Agents: {data[\"agents_installed\"]}')
print(f'Mémoire: {data[\"memory_usage\"]}')
"
    else
        echo -e "API REST: ${RED}❌ HORS LIGNE${NC}"
    fi
    
    # Vérifier dashboard
    if curl -s http://localhost:5001 > /dev/null 2>&1; then
        echo -e "Dashboard: ${GREEN}✅ EN LIGNE (port 5001)${NC}"
    else
        echo -e "Dashboard: ${RED}❌ HORS LIGNE${NC}"
    fi
    
    # Vérifier processus Python
    echo -e "\nProcessus actifs:"
    ps aux | grep -E "python.*(api|dashboard)" | grep -v grep || echo "  Aucun"
}

start_all() {
    echo -e "\n${BLUE}=== DÉMARRAGE COMPLET ===${NC}"
    
    # Démarrer API REST
    echo "1. Démarrage API REST..."
    cd /root
    python3 api_rest_agents.py > /var/log/ia_api.log 2>&1 &
    sleep 3
    
    # Démarrer Dashboard
    echo "2. Démarrage Dashboard..."
    python3 agent_dashboard.py > /var/log/ia_dashboard.log 2>&1 &
    sleep 2
    
    check_status
}

stop_all() {
    echo -e "\n${BLUE}=== ARRÊT COMPLET ===${NC}"
    pkill -f "api_rest_agents.py"
    pkill -f "agent_dashboard.py"
    sleep 2
    echo "Système arrêté."
}

show_menu() {
    while true; do
        echo -e "\n${BLUE}=== PANEL DE CONTRÔLE - AGENTS IA ===${NC}"
        echo "1. Vérifier l'état du système"
        echo "2. Démarrer tout (API + Dashboard)"
        echo "3. Arrêter tout"
        echo "4. Accéder à l'API REST (port 5002)"
        echo "5. Accéder au Dashboard (port 5001)"
        echo "6. Lister tous les agents"
        echo "7. Tester un agent spécifique"
        echo "8. Voir les logs"
        echo "9. Quitter"
        
        read -p "Choix: " choice
        
        case $choice in
            1) check_status ;;
            2) start_all ;;
            3) stop_all ;;
            4) 
                echo "Accès API: http://localhost:5002/api/agents"
                curl -s http://localhost:5002/api/agents | python3 -m json.tool | head -50
                ;;
            5)
                echo "Dashboard: http://localhost:5001"
                echo "Ouvrez cette URL dans votre navigateur"
                ;;
            6)
                echo -e "\n${GREEN}Liste des agents:${NC}"
                ls -la /root/*.py | grep -i agent
                echo -e "\n${GREEN}Scripts disponibles:${NC}"
                ls -la /root/*.sh
                ;;
            7)
                read -p "Nom de l'agent (.py): " agent
                if [ -f "/root/$agent" ]; then
                    echo -e "\nContenu de $agent:"
                    head -20 "/root/$agent"
                else
                    echo "Fichier non trouvé"
                fi
                ;;
            8)
                echo -e "\n${GREEN}Logs API:${NC}"
                tail -10 /var/log/ia_api.log 2>/dev/null || echo "Pas de logs"
                echo -e "\n${GREEN}Logs Dashboard:${NC}"
                tail -10 /var/log/ia_dashboard.log 2>/dev/null || echo "Pas de logs"
                ;;
            9) exit 0 ;;
            *) echo "Choix invalide" ;;
        esac
    done
}

# Vérifier les dépendances
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installation des dépendances..."
    pip3 install flask requests
fi

show_menu
EOF

chmod +x /root/control_panel.sh
