cat > flask_control.sh << 'EOF'
#!/bin/sh
echo "=== Contrôle Flask ==="
echo "1. Vérifier l'environnement"
echo "2. Démarrer le serveur"
echo "3. Arrêter le serveur"
echo "4. Voir les processus"
echo "Q. Quitter"
read -p "Choix: " choice

case $choice in
    1)
        python3 -c "import sys, flask; print(f'Python {sys.version.split()[0]}, Flask {flask.__version__}')"
        ;;
    2)
        echo "Démarrage sur http://127.0.0.1:5000"
        python3 -m flask run --host=0.0.0.0 --port=5000 &
        ;;
    3)
        pkill -f flask
        echo "Serveurs Flask arrêtés"
        ;;
    4)
        ps aux | grep flask | grep -v grep
        ;;
    q|Q)
        exit 0
        ;;
    *)
        echo "Option invalide"
        ;;
esac
EOF
