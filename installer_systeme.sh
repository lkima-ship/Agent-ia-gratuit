cat > installer_systeme.sh << 'EOF'
#!/bin/bash
echo "📥 Installation du système d'organisation..."

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    echo "📦 Installation de Python3..."
    apk add python3 py3-pip
fi

# Télécharger l'organisateur
echo "📦 Téléchargement de l'organisateur..."
curl -s https://raw.githubusercontent.com/ton_utilisateur/organisateur/main/organiseur_intelligent.py -o organiseur_intelligent.py

# Exécuter
echo "🚀 Exécution de l'organisateur..."
python3 organiseur_intelligent.py

echo "✅ Installation terminée!"
EOF

chmod +x installer_systeme.sh
./installer_systeme.sh
