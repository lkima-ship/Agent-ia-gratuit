#!/bin/ash

echo "=== MENU FLASK iSH ==="
echo "1. Démarrer le serveur Flask"
echo "2. Tester avec curl"
echo "3. Générer rapport HTML"
echo "4. Voir l'adresse IP"
echo "5. Vérifier si le serveur tourne"
echo "6. Arrêter le serveur"
echo "7. Quitter"

read -p "Votre choix: " choice

case $choice in
    1)
        echo "Démarrage du serveur Flask..."
        # Vérifier si un serveur est déjà en cours
        if ps aux | grep -v grep | grep "python3 /root/app.py" > /dev/null; then
            echo "⚠️  Un serveur est déjà en cours d'exécution"
            echo "Utilisez l'option 6 pour l'arrêter d'abord"
        else
            python3 /root/app.py &
            echo "✅ Serveur démarré en arrière-plan"
            echo "Attendez 3 secondes avant de tester..."
            sleep 3
        fi
        ;;
    2)
        echo "Test avec curl..."
        echo "Résultat :"
        curl -s -o /dev/null -w "Code HTTP: %{http_code}\nTemps: %{time_total}s\n" http://127.0.0.1:5000
        echo "--- Contenu de la réponse ---"
        curl http://127.0.0.1:5000 2>/dev/null || echo "❌ Impossible de se connecter"
        ;;
    3)
        echo "Génération du rapport..."
        python3 /root/generate_report.py
        ;;
    4)
        echo "Adresse IP locale: 127.0.0.1"
        echo "Pour accéder depuis un autre appareil, vous avez besoin de l'IP WiFi"
        echo "Note: iSH a des limitations réseau sur iOS"
        ;;
    5)
        echo "Vérification des processus..."
        if ps aux | grep -v grep | grep "python3 /root/app.py" > /dev/null; then
            echo "✅ Serveur Flask en cours d'exécution"
            echo "Processus:"
            ps aux | grep -v grep | grep "python3 /root/app.py"
        else
            echo "❌ Aucun serveur Flask en cours d'exécution"
        fi
        ;;
    6)
        echo "Arrêt du serveur..."
        pkill -f flask 2>/dev/null && echo "✅ Serveur arrêté" || echo "❌ Aucun serveur à arrêter"
        ;;
    7)
        echo "Au revoir!"
        exit 0
        ;;
    *)
        echo "Choix invalide"
        ;;
esac

echo ""
read -p "Appuyez sur Entrée pour continuer..."
./flask_menu.sh
