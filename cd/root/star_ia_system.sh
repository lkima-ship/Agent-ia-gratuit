# Créer un lanceur simple
cat > /root/start_ai_system.sh << 'EOF'
#!/bin/sh
# Lanceur universel ASH-compatible

echo ""
echo "🤖 SYSTÈME IA - ALPINE LINUX"
echo "============================="
echo ""

cd /root 2>/dev/null || {
    echo "❌ Impossible d'accéder à /root"
    exit 1
}

while :; do
    echo ""
    echo "MENU PRINCIPAL:"
    echo "1. 🌐 Interface Web (port 8080)"
    echo "2. 🧠 Agent Cognitif"
    echo "3. 📊 Agent IA ML (original)"
    echo "4. 🔧 Vérifier les fichiers"
    echo "5. 📁 Lister les agents"
    echo "0. 🚪 Quitter"
    echo ""
    
    printf "👉 Votre choix: "
    read choix
    
    case "$choix" in
        1)
            echo "Lancement de l'interface web..."
            if [ -f "web_interface.py" ] && [ -s "web_interface.py" ]; then
                python3 web_interface.py &
                PID=$!
                echo "✅ Serveur démarré (PID: $PID)"
                echo "🌐 Accès: http://localhost:8080"
                echo "🛑 Pour arrêter: kill $PID"
            else
                echo "❌ web_interface.py non trouvé ou vide"
            fi
            ;;
        2)
            echo "Lancement de l'agent cognitif..."
            if [ -f "agent_cognitif.py" ] && [ -s "agent_cognitif.py" ]; then
                python3 agent_cognitif.py
            else
                echo "❌ agent_cognitif.py non trouvé ou vide"
            fi
            ;;
        3)
            echo "Lancement de l'agent IA ML..."
            if [ -f "agent_ia_ml.py" ] && [ -s "agent_ia_ml.py" ]; then
                python3 agent_ia_ml.py
            else
                echo "❌ agent_ia_ml.py non trouvé"
            fi
            ;;
        4)
            echo "Vérification des fichiers..."
            echo "Fichiers Python dans /root:"
            ls -la *.py 2>/dev/null | head -10
            echo ""
            echo "Taille des fichiers clés:"
            for f in web_interface.py agent_cognitif.py agent_ia_ml.py; do
                if [ -f "$f" ]; then
                    size=$(wc -c < "$f" 2>/dev/null || echo "0")
                    echo "  $f: $size octets"
                else
                    echo "  $f: MANQUANT"
                fi
            done
            ;;
        5)
            echo "Agents disponibles:"
            ls *.py 2>/dev/null | grep -i agent | head -15
            ;;
        0)
            echo "Au revoir!"
            exit 0
            ;;
        *)
            echo "Choix invalide"
            ;;
    esac
    
    echo ""
    printf "↵ Appuyez sur Entrée pour continuer... "
    read dummy
done
EOF

# Rendre exécutable et lancer
chmod +x /root/start_ai_system.sh
/root/start_ai_system.sh
