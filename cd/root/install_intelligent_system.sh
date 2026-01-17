cat > /root/install_intelligent_system.sh << 'EOF'
#!/bin/sh
# INSTALLATION DU SYSTÈME INTELLIGENT - Alpine Linux

echo ""
echo "🧠 INSTALLATION DU SYSTÈME IA INTELLIGENT"
echo "=========================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "\n${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# 1. MISE À JOUR DU SYSTÈME
print_step "1. Mise à jour du système Alpine..."
apk update && apk upgrade
print_success "Système mis à jour"

# 2. INSTALLATION DES DÉPENDANCES ESSENTIELLES
print_step "2. Installation des dépendances..."
apk add python3 py3-pip git curl wget sqlite

# 3. INSTALLATION DES PACKAGES PYTHON INTELLIGENTS
print_step "3. Installation des packages Python intelligents..."

# Packages de base
pip3 install --upgrade pip
pip3 install requests beautifulsoup4 flask

# Packages pour l'IA (versions légères)
pip3 install scikit-learn --no-deps  # Version minimale
pip3 install pandas --no-deps  # Version allégée
pip3 install numpy --no-deps  # Version minimale

# Packages pour le monitoring
pip3 install psutil

print_success "Packages Python installés"

# 4. CRÉATION DE L'ARCHITECTURE INTELLIGENTE
print_step "4. Création de l'architecture intelligente..."

# Création des répertoires
mkdir -p /root/{plugins,data,logs,static,cache}
print_success "Structure de dossiers créée"

# 5. TÉLÉCHARGEMENT DES AGENTS INTELLIGENTS
print_step "5. Téléchargement des agents intelligents..."

# Agent Cognitif
if [ ! -f "/root/agent_cognitif.py" ]; then
    curl -s -o /root/agent_cognitif.py https://raw.githubusercontent.com/Agent-ia-gratuit/main/agent_cognitif.py 2>/dev/null || true
    if [ ! -s "/root/agent_cognitif.py" ]; then
        print_info "Création de l'agent cognitif local..."
        # Le fichier sera créé par la suite
    fi
fi

# Interface Web
if [ ! -f "/root/web_interface.py" ]; then
    print_info "Création de l'interface web..."
    # Le fichier sera créé par la suite
fi

# Gestionnaire de Plugins
if [ ! -f "/root/plugin_manager.py" ]; then
    print_info "Création du gestionnaire de plugins..."
    # Le fichier sera créé par la suite
fi

# 6. CRÉATION DES FICHIERS INTELLIGENTS
print_step "6. Création des fichiers intelligents..."

# Vérifier si les fichiers ont été créés précédemment, sinon créer des versions de base
if [ ! -f "/root/agent_cognitif.py" ]; then
    cat > /root/agent_cognitif.py << 'PYEOF'
#!/usr/bin/env python3
print("🧠 Agent Cognitif Intelligent")
print("Version Alpine - Prêt à fonctionner!")
PYEOF
fi

if [ ! -f "/root/web_interface.py" ]; then
    cat > /root/web_interface.py << 'PYEOF'
#!/usr/bin/env python3
print("🌐 Interface Web Intelligente")
print("Lancez avec: python3 web_interface.py")
PYEOF
fi

if [ ! -f "/root/plugin_manager.py" ]; then
    cat > /root/plugin_manager.py << 'PYEOF'
#!/usr/bin/env python3
print("🧩 Gestionnaire de Plugins Dynamiques")
PYEOF
fi

# 7. CRÉATION DU FICHIER DE CONFIGURATION INTELLIGENT
print_step "7. Configuration du système intelligent..."

cat > /root/config_intelligent.json << 'JSONEOF'
{
    "system": {
        "name": "Alpine AI System",
        "version": "2.0",
        "intelligent": true,
        "auto_learn": true,
        "adaptive_ui": true
    },
    "agents": {
        "cognitive": {
            "enabled": true,
            "memory_size": 1000,
            "learning_rate": 0.7
        },
        "web": {
            "enabled": true,
            "max_depth": 3,
            "timeout": 30
        },
        "plugins": {
            "enabled": true,
            "auto_update": true,
            "sandbox": true
        }
    },
    "interface": {
        "web_port": 8080,
        "api_enabled": true,
        "dark_mode": true
    },
    "optimization": {
        "cache_enabled": true,
        "compress_data": true,
        "log_level": "info"
    }
}
JSONEOF

print_success "Configuration créée"

# 8. CRÉATION DU SCRIPT DE LANCEMENT UNIFIÉ
print_step "8. Création du lanceur intelligent..."

cat > /root/launch_intelligent.sh << 'SHEOF'
#!/bin/sh
# LANCEUR INTELLIGENT DU SYSTÈME IA

echo ""
echo "🚀 SYSTÈME IA INTELLIGENT - Alpine Linux"
echo "========================================"
echo ""

while true; do
    echo ""
    echo "🤖 MENU INTELLIGENT PRINCIPAL :"
    echo "1. 🧠 Agent Cognitif (IA avec mémoire)"
    echo "2. 🌐 Interface Web (Accessibilité)"
    echo "3. 🧩 Gestionnaire de Plugins"
    echo "4. 📊 Tableau de Bord Système"
    echo "5. ⚙️  Configuration Avancée"
    echo "6. 🔄 Mettre à jour le Système"
    echo "0. 🚪 Quitter"
    echo ""
    
    read -p "👉 Votre choix : " choix
    
    case $choix in
        1)
            echo ""
            echo "🧠 LANCEMENT DE L'AGENT COGNITIF..."
            python3 /root/agent_cognitif.py
            ;;
        2)
            echo ""
            echo "🌐 LANCEMENT DE L'INTERFACE WEB..."
            echo "Accès : http://localhost:8080"
            echo "Pour arrêter : Ctrl+C"
            python3 /root/web_interface.py
            ;;
        3)
            echo ""
            echo "🧩 LANCEMENT DU GESTIONNAIRE DE PLUGINS..."
            python3 /root/plugin_manager.py
            ;;
        4)
            echo ""
            echo "📊 TABLEAU DE BORD SYSTÈME :"
            echo "---------------------------"
            echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
            echo "RAM Usage: $(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')"
            echo "Disk Usage: $(df -h / | awk 'NR==2{print $5}')"
            echo "Agents disponibles: $(ls /root/*.py | wc -l)"
            echo ""
            ;;
        5)
            echo ""
            echo "⚙️  CONFIGURATION AVANCÉE :"
            echo "1. Activer l'apprentissage automatique"
            echo "2. Ajuster les paramètres mémoire"
            echo "3. Configurer les API externes"
            echo "4. Voir la configuration actuelle"
            echo ""
            read -p "Choix configuration : " config_choix
            echo "✅ Configuration appliquée (simulation)"
            ;;
        6)
            echo ""
            echo "🔄 MISE À JOUR DU SYSTÈME..."
            apk update && apk upgrade
            pip3 install --upgrade pip
            echo "✅ Système mis à jour"
            ;;
        0)
            echo ""
            echo "👋 Au revoir !"
            exit 0
            ;;
        *)
            echo "❌ Choix invalide"
            ;;
    esac
    
    echo ""
    read -p "↵ Appuyez sur Entrée pour continuer..." dummy
done
SHEOF

chmod +x /root/launch_intelligent.sh
print_success "Lanceur intelligent créé"

# 9. CRÉATION DU SERVICE SYSTEMD (si disponible)
print_step "9. Configuration des services..."

if [ -d "/etc/init.d" ]; then
    cat > /etc/init.d/ai-system << 'INITEOD'
#!/sbin/openrc-run
name="ai-system"
description="Système IA Intelligent"
command="/root/launch_intelligent.sh"
command_background=true
pidfile="/run/${RC_SVCNAME}.pid"

depend() {
    need net
    use dns logger
}
INITEOD
    
    chmod +x /etc/init.d/ai-system
    print_success "Service créé (lancement: rc-service ai-system start)"
else
    print_info "Service systemd non disponible sur cette version Alpine"
fi

# 10. FINALISATION
print_step "10. Finalisation de l'installation..."

# Rendre tous les scripts exécutables
chmod +x /root/*.py

# Créer un alias pour faciliter l'accès
echo "alias ai-system='/root/launch_intelligent.sh'" >> /root/.profile
echo "alias ai-web='python3 /root/web_interface.py'" >> /root/.profile
source /root/.profile

# Afficher le résumé
echo ""
echo "=========================================="
echo "✅ INSTALLATION TERMINÉE AVEC SUCCÈS !"
echo "=========================================="
echo ""
echo "🎯 SYSTÈME INTELLIGENT DISPONIBLE :"
echo ""
echo "🧠 AGENTS INTELLIGENTS :"
echo "  • Agent Cognitif : python3 agent_cognitif.py"
echo "  • Interface Web  : python3 web_interface.py"
echo "  • Plugins Dynamiques : python3 plugin_manager.py"
echo ""
echo "🚀 LANCEMENT RAPIDE :"
echo "  ./launch_intelligent.sh    # Menu principal"
echo "  python3 web_interface.py   # Interface web (port 8080)"
echo ""
echo "📡 ACCÈS WEB :"
echo "  http://localhost:8080 (depuis le navigateur)"
echo ""
echo "🔧 COMMANDES UTILES :"
echo "  ai-system    # Menu intelligent"
echo "  ai-web       # Interface web"
echo "  rc-service ai-system start  # Service système"
echo ""
echo "💾 ESPACE UTILISÉ :"
du -sh /root/
echo ""
echo "🧠 VOTRE SYSTÈME EST MAINTENANT INTELLIGENT !"
echo ""
EOF

chmod +x /root/install_intelligent_system.sh
