cat > /root/check_dependencies.py << 'EOF'
#!/usr/bin/env python3
"""
Vérifie et installe les dépendances pour tous les agents
"""

import os
import sys
import subprocess

DEPENDENCIES = [
    "requests>=2.28.0",
    "beautifulsoup4>=4.11.0",
    "pandas>=1.5.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.2.0",
    "openai>=0.27.0",
    "python-dotenv>=1.0.0",
    "flask>=2.3.0",
    "fastapi>=0.95.0",
    "uvicorn>=0.21.0",
    "psutil>=5.9.0",
    "paramiko>=3.1.0",
    "selenium>=4.9.0",
    "playwright",
    "pytz>=2023.0",
    "colorama>=0.4.0"
]

def verifier_python():
    """Vérifie la version de Python"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 ou supérieur requis")
        return False
    return True

def installer_dependances():
    """Installe les dépendances manquantes"""
    print("\n📦 Installation des dépendances...")
    
    for dep in DEPENDENCIES:
        try:
            # Essayer d'importer
            if ">=" in dep:
                package = dep.split(">=")[0]
            else:
                package = dep
            
            __import__(package.replace("-", "_"))
            print(f"✅ {package} déjà installé")
        except ImportError:
            print(f"📦 Installation de {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} installé avec succès")
            except:
                print(f"⚠️  Échec d'installation de {dep}")
    
    # Installer Playwright browsers
    try:
        print("\n🌐 Installation des navigateurs pour Playwright...")
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("✅ Navigateurs installés")
    except:
        print("⚠️  Playwright non installé ou erreur d'installation")

def creer_structure_dossiers():
    """Crée la structure de dossiers nécessaire"""
    print("\n📁 Création de la structure de dossiers...")
    
    dossiers = [
        "/root/logs",
        "/root/data",
        "/root/.cache",
        "/root/configs",
        "/root/models",
        "/root/temp"
    ]
    
    for dossier in dossiers:
        try:
            os.makedirs(dossier, exist_ok=True)
            print(f"✓ Dossier {dossier} créé")
        except Exception as e:
            print(f"⚠️  Erreur création {dossier}: {e}")

def main():
    print("🔍 VÉRIFICATION DU SYSTÈME")
    print("="*50)
    
    # Vérifier Python
    if not verifier_python():
        sys.exit(1)
    
    # Créer structure
    creer_structure_dossiers()
    
    # Installer dépendances
    installer_dependances()
    
    print("\n" + "="*50)
    print("✅ SYSTÈME PRÊT !")
    print("Tous les agents peuvent maintenant être exécutés.")
    print("\nLancez le menu principal avec:")
    print("  python3 agent_ia_ml.py")
    print("  ou")
    print("  python3 menu_master_v2.py")

if __name__ == "__main__":
    main()
EOF
