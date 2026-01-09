@echo off
echo 🚀 Installation de l'Agent IA Professionnel

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    pause
    exit /b 1
)

REM Créer environnement virtuel
echo 📦 Création de l'environnement virtuel...
python -m venv venv

REM Activer
call venv\Scripts\activate.bat

REM Mettre à jour pip
python -m pip install --upgrade pip

REM Installer dépendances
echo 📦 Installation des dépendances...
pip install -r requirements.txt

REM Configurer
echo ⚙️ Configuration...
if not exist ".env" (
    copy .env.example .env
    echo ⚠️  Éditez le fichier .env avec vos informations
)

REM Créer dossiers de stockage
if not exist "storage" mkdir storage
if not exist "storage\logs" mkdir storage\logs

echo ✅ Installation terminée!
echo 👉 Pour lancer: venv\Scripts\activate && python main.py
pause
