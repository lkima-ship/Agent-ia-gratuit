cat > /root/launch_agents.sh << 'EOF'
#!/bin/bash
# Script de lancement unifié pour tous les agents

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonctions
print_header() {
    echo -e "${BLUE}"
    echo "=========================================="
    echo "   AGENT IA SYSTEM - MENU DE LANCEMENT    "
    echo "=========================================="
    echo -e "${NC}"
}

print_menu() {
    echo -e "\n${YELLOW}📋 AGENTS DISPONIBLES :${NC}"
    echo "1. 🚀 Agent IA ML (Principal)"
    echo "2. 📊 Analyse Données"
    echo "3. 🌐 Agent Web Avancé V2"
    echo "4. 🔍 Agent Web Simple"
    echo "5. 🤖 Agent IA Pro"
    echo "6. 🆓 Agent IA Gratuit"
    echo "7. 📦 Agent IA Complet"
    echo "8. 🏠 Hub Agents"
    echo "9. ⚙️  Surveillance Système"
    echo "10. 🎛️ Menu Master V2"
    echo "11. 🔧 Vérifier Dépendances"
    echo "12. 📁 Explorer Fichiers"
    echo "0. ❌ Quitter"
    echo -e "\n${YELLOW}==========================================${NC}"
}

check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $2"
        return 0
    else
        echo -e "${RED}✗${NC} $2 (fichier manquant)"
        return 1
    fi
}

# Vérifier tous les fichiers
check_all_files() {
    echo -e "\n${YELLOW}🔍 Vérification des fichiers...${NC}"
    check_file "/root/agent_ia_ml.py" "Agent IA ML"
    check_file "/root/agent_analyse_donnees.py" "Analyse Données"
    check_file "/root/agent_web_avance_v2.py" "Agent Web Avancé V2"
    check_file "/root/agent_web_avance.py" "Agent Web Simple"
    check_file "/root/agent_ia_pro.py" "Agent IA Pro"
    check_file "/root/agent_ia_gratuit.py" "Agent IA Gratuit"
    check_file "/root/agent_ia_complet.py" "Agent IA Complet"
    check_file "/root/hub_agents.py" "Hub Agents"
    check_file "/root/agent_surveillance.py" "Surveillance Système"
    check_file "/root/menu_master_v2.py" "Menu Master V2"
}

# Menu principal
while true; do
    clear
    print_header
    print_menu
    
    read -p "👉 Votre choix (0-12) : " choix
    
    case $choix in
        1)
            echo -e "\n${GREEN}🚀 Lancement de l'Agent IA ML...${NC}"
            cd /root && python3 agent_ia_ml.py
            ;;
        2)
            echo -e "\n${GREEN}📊 Lancement de l'Analyse Données...${NC}"
            cd /root && python3 agent_analyse_donnees.py
            ;;
        3)
            echo -e "\n${GREEN}🌐 Lancement de l'Agent Web Avancé V2...${NC}"
            cd /root && python3 agent_web_avance_v2.py
            ;;
        4)
            echo -e "\n${GREEN}🔍 Lancement de l'Agent Web Simple...${NC}"
            cd /root && python3 agent_web_avance.py
            ;;
        5)
            echo -e "\n${GREEN}🤖 Lancement de l'Agent IA Pro...${NC}"
            cd /root && python3 agent_ia_pro.py
            ;;
        6)
            echo -e "\n${GREEN}🆓 Lancement de l'Agent IA Gratuit...${NC}"
            cd /root && python3 agent_ia_gratuit.py
            ;;
        7)
            echo -e "\n${GREEN}📦 Lancement de l'Agent IA Complet...${NC}"
            cd /root && python3 agent_ia_complet.py
            ;;
        8)
            echo -e "\n${GREEN}🏠 Lancement du Hub Agents...${NC}"
            cd /root && python3 hub_agents.py
            ;;
        9)
            echo -e "\n${GREEN}⚙️  Lancement de la Surveillance Système...${NC}"
            cd /root && python3 agent_surveillance.py
            ;;
        10)
            echo -e "\n${GREEN}🎛️  Lancement du Menu Master V2...${NC}"
            cd /root && python3 menu_master_v2.py
            ;;
        11)
            echo -e "\n${GREEN}🔧 Vérification des dépendances...${NC}"
            cd /root && python3 check_dependencies.py
            read -p "Appuyez sur Entrée pour continuer..."
            ;;
        12)
            echo -e "\n${GREEN}📁 Exploration des fichiers...${NC}"
            ls -la /root/*.py
            echo -e "\n${YELLOW}--- FICHIERS PYTHON ---${NC}"
            find /root -name "*.py" -type f | head -20
            read -p "Appuyez sur Entrée pour continuer..."
            ;;
        0)
            echo -e "\n${GREEN}👋 Au revoir !${NC}"
            exit 0
            ;;
        *)
            echo -e "\n${RED}❌ Choix invalide${NC}"
            sleep 1
            ;;
    esac
    
    if [ $choix -ne 0 ]; then
        echo -e "\n${YELLOW}↵ Appuyez sur Entrée pour retourner au menu...${NC}"
        read
    fi
done
EOF

# Rendre exécutable
chmod +x /root/launch_agents.sh
chmod +x /root/check_dependencies.py
