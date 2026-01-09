#!/bin/bash
# setup.sh - Crée toute la structure

echo "🚀 Création de la structure..."

# Crée tous les dossiers
mkdir -p .github/workflows
mkdir -p src/{modules,utils,web/templates,api,bots}
mkdir -p {tests,docs,scripts,data/{emails,voice,logs},examples,config}

# Crée les fichiers principaux
touch .env.example .gitignore requirements.txt Dockerfile README.md LICENSE

# Crée les fichiers Python
touch src/{main.py,web_app.py,api_server.py}
touch src/modules/{__init__.py,ai_processor.py,email_handler.py,calendar_manager.py,voice_processor.py,database.py}
touch src/utils/{__init__.py,config_loader.py,logger.py,helpers.py,setup_wizard.py,backup.py}
touch src/web/{__init__.py,dashboard.py}
touch src/web/templates/base.html
touch src/api/{__init__.py,routes.py,models.py}
touch src/bots/{telegram_bot.py,discord_bot.py}

# Crée autres fichiers
touch docs/{installation.md,usage.md,api.md,faq.md}
touch scripts/{install.sh,install.bat,setup.py}
touch examples/{basic_usage.py,custom_module.py}
touch config/{default.yaml,production.yaml}

echo "✅ Structure créée !"
echo "📁 Dossier : assistant-ia-gratuit"
