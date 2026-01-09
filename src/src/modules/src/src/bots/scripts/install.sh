#!/bin/bash

echo "🚀 Installation Assistant IA Gratuit"

# Vérifier Python
python3 --version || { echo "❌ Python 3 requis"; exit 1; }

# Créer environnement
python3 -m venv venv
source venv/bin/activate

# Installer dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Configurer
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "📝 Éditez le fichier .env avec vos clés API"
fi

echo "✅ Installation terminée !"
echo "👉 source venv/bin/activate"
echo "👉 python src/main.py"
