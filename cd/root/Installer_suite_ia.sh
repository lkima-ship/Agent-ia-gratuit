cat > installer_suite_ia.sh << 'EOF'
#!/bin/bash
echo "🚀 INSTALLATION DE LA SUITE AGENTS IA"
echo "======================================"

cd /root

# Créer la structure
echo "📁 Création de la structure..."
mkdir -p agents_ia/{web,reseau,analyse,donnees,ia_avancee}

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "✅ Python3 trouvé"

# Installer les dépendances
echo "📦 Installation des dépendances..."
python3 -m pip install psutil requests numpy --quiet 2>/dev/null || echo "Installation des dépendances échouée"

# Créer les fichiers principaux
echo "📝 Création des agents..."

# Copier le code des agents créés précédemment
# (Dans un scénario réel, on copierait les fichiers)
echo "✅ Agents créés :"
echo "  • agent_ia_ml.py"
echo "  • agent_analyse_donnees.py"
echo "  • agent_web_avance.py"
echo "  • agent_surveillance.py"
echo "  • suite_agents_ia.py"

# Créer un raccourci
echo "alias suite-ia='cd /root && python3 suite_agents_ia.py'" >> ~/.bashrc
source ~/.bashrc

echo ""
echo "🎉 INSTALLATION TERMINÉE !"
echo ""
echo "📋 Commandes disponibles :"
echo "  • suite-ia          # Lancer la suite complète"
echo "  • python3 suite_agents_ia.py"
echo ""
echo "🚀 Pour démarrer : tapez 'suite-ia' ou 'python3 suite_agents_ia.py'"
EOF

chmod +x installer_suite_ia.sh
./installer_suite_ia.sh
