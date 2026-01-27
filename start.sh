# Créez un script de démarrage rapide
cat > start.sh << 'EOF'
#!/bin/bash
echo "🚀 Démarrage du système IA..."
echo "Agents disponibles:"
ls AGENTS/ | head -5
echo ""
echo "Pour utiliser le menu: python3 menu.py"
echo "Pour lancer un agent: python3 AGENTS/nom_de_l_agent.py"
EOF

chmod +x start.sh
./start.sh
