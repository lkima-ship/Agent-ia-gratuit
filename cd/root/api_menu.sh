# /root/api_menu.sh
#!/bin/bash

while true; do
    clear
    echo "=== CONTRÔLE API FLASK ==="
    echo "1. Démarrer l'API"
    echo "2. Arrêter l'API"
    echo "3. Vérifier le statut"
    echo "4. Voir les logs"
    echo "5. Tester l'API"
    echo "6. Quitter"
    echo -n "Votre choix: "
    
    read choice
    
    case $choice in
        1)
            echo "Démarrage..."
            pkill -f python 2>/dev/null
            python3 /root/simple_working.py 2>&1 > /tmp/api.log &
            echo "API démarrée"
            sleep 2
            ;;
        2)
            echo "Arrêt..."
            pkill -f python 2>/dev/null
            echo "API arrêtée"
            ;;
        3)
            if pgrep -f "simple_working.py" > /dev/null; then
                echo "✅ API en cours d'exécution"
            else
                echo "❌ API arrêtée"
            fi
            ;;
        4)
            echo "=== Dernières lignes des logs ==="
            tail -20 /tmp/api.log
            ;;
        5)
            echo "Test de l'API..."
            curl -s http://localhost:5002 && echo ""
            ;;
        6)
            echo "Au revoir!"
            exit 0
            ;;
        *)
            echo "Choix invalide"
            ;;
    esac
    
    echo "Appuyez sur Entrée pour continuer..."
    read
done
