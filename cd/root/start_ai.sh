cat > /root/start_ai.sh << 'EOF'
#!/bin/sh
echo ""
echo "🚀 SYSTÈME IA - LANCEUR UNIVERSEL"
echo "================================="
echo "Répertoire: $(pwd)"
echo ""

# Vérifier les fichiers essentiels
ESSENTIAL_FILES=0

if [ -f "/root/web_interface.py" ]; then
    echo "✅ web_interface.py trouvé"
    ESSENTIAL_FILES=$((ESSENTIAL_FILES + 1))
else
    echo "❌ web_interface.py manquant"
fi

if [ -f "/root/agent_cognitif.py" ]; then
    echo "✅ agent_cognitif.py trouvé"
    ESSENTIAL_FILES=$((ESSENTIAL_FILES + 1))
else
    echo "❌ agent_cognitif.py manquant"
fi

if [ -f "/root/agent_ia_ml.py" ]; then
    echo "✅ agent_ia_ml.py trouvé"
    ESSENTIAL_FILES=$((ESSENTIAL_FILES + 1))
else
    echo "❌ agent_ia_ml.py manquant"
fi

echo ""
if [ $ESSENTIAL_FILES -lt 2 ]; then
    echo "⚠️  Certains fichiers manquent. Exécutez d'abord :"
    echo "    /root/fix_filenames.sh"
    exit 1
fi

echo "🤖 MENU PRINCIPAL :"
echo "1. 🌐 Interface Web (port 8080)"
echo "2. 🧠 Agent Cognitif Intelligent"
echo "3. 📊 Menu Original Agents IA"
echo "4. 🔧 Tester tous les agents"
echo "5. 📁 Lister tous les agents"
echo "0. 🚪 Quitter"
echo ""

while true; do
    printf "👉 Votre choix : "
    read choix
    
    case $choix in
        1)
            echo ""
            echo "🌐 LANCEMENT DE L'INTERFACE WEB..."
            echo "Accès : http://localhost:8080"
            echo "Arrêt : Ctrl+C"
            echo ""
            python3 /root/web_interface.py
            ;;
        2)
            echo ""
            echo "🧠 LANCEMENT DE L'AGENT COGNITIF..."
            python3 /root/agent_cognitif.py
            ;;
        3)
            echo ""
            echo "📊 LANCEMENT DU MENU ORIGINAL..."
            python3 /root/agent_ia_ml.py
            ;;
        4)
            echo ""
            echo "🔧 TEST DE TOUS LES AGENTS..."
            for agent in web_interface.py agent_cognitif.py agent_ia_ml.py; do
                if [ -f "/root/$agent" ]; then
                    echo "Test de $agent :"
                    python3 "/root/$agent" --version 2>&1 | head -1 || echo "  ✅ Fonctionne"
                fi
            done
            ;;
        5)
            echo ""
            echo "📁 AGENTS DISPONIBLES :"
            ls /root/*.py | xargs -n1 basename | grep -i agent
            echo ""
            echo "Total : $(ls /root/*.py | wc -l) fichiers Python"
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
    printf "↵ Appuyez sur Entrée pour continuer... "
    read dummy
done
EOF

chmod +x /root/start_ai.sh
/root/start_ai.sh
