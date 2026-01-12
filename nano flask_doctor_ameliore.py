#!/usr/bin/env python3
"""
Diagnostic Flask Amélioré - Vérification complète de l'environnement
"""

import sys
import os
import subprocess
from datetime import datetime

def print_header(title):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_success(message):
    """Affiche un message de succès"""
    print(f"  ✅ {message}")

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"  ❌ {message}")

def print_warning(message):
    """Affiche un message d'avertissement"""
    print(f"  ⚠️  {message}")

def print_info(message):
    """Affiche un message informatif"""
    print(f"  ℹ️  {message}")

def check_python_version():
    """Vérifie la version de Python"""
    print_header("VÉRIFICATION PYTHON")
    print_info(f"Version Python: {sys.version}")
    print_info(f"Chemin Python: {sys.executable}")
    return sys.version_info >= (3, 6)

def check_flask_installation():
    """Vérifie l'installation de Flask"""
    print_header("VÉRIFICATION FLASK")
    
    try:
        import flask
        print_success(f"Flask est installé (version: {flask.__version__})")
        return True
    except ImportError as e:
        print_error(f"Flask n'est pas installé: {e}")
        return False

def check_flask_dependencies():
    """Vérifie les dépendances de Flask"""
    print_header("DÉPENDANCES FLASK")
    
    dependencies = [
        'werkzeug',
        'jinja2',
        'itsdangerous',
        'click',
        'markupsafe'
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            module = __import__(dep)
            version = getattr(module, '__version__', 'Version inconnue')
            print_success(f"{dep}: {version}")
        except ImportError:
            print_error(f"{dep}: NON INSTALLÉ")
            all_ok = False
    
    return all_ok

def check_virtual_environment():
    """Vérifie si on est dans un environnement virtuel"""
    print_header("ENVIRONNEMENT VIRTUEL")
    
    in_venv = sys.prefix != sys.base_prefix
    if in_venv:
        print_success(f"Environnement virtuel actif: {sys.prefix}")
    else:
        print_warning("Pas d'environnement virtuel détecté")
    
    return in_venv

def check_project_structure():
    """Vérifie la structure du projet Flask"""
    print_header("STRUCTURE DU PROJET")
    
    important_files = [
        'app.py',
        'run.py',
        'application.py',
        'wsgi.py'
    ]
    
    flask_folders = [
        'templates',
        'static',
        'instance'
    ]
    
    found_files = []
    for file in important_files:
        if os.path.exists(file):
            found_files.append(file)
            print_success(f"Fichier trouvé: {file}")
    
    found_folders = []
    for folder in flask_folders:
        if os.path.exists(folder) and os.path.isdir(folder):
            found_folders.append(folder)
            print_success(f"Dossier trouvé: {folder}/")
    
    if not found_files:
        print_warning("Aucun fichier principal Flask trouvé")
    
    return len(found_files) > 0

def test_flask_app():
    """Teste la création d'une application Flask simple"""
    print_header("TEST D'APPLICATION FLASK")
    
    try:
        from flask import Flask
        app = Flask(__name__)
        
        @app.route('/test')
        def test():
            return 'OK'
        
        print_success("Application Flask créée avec succès")
        
        # Vérification des configurations
        print_info(f"Debug mode: {app.debug}")
        print_info(f"Testing mode: {app.testing}")
        
        return True
    except Exception as e:
        print_error(f"Erreur lors de la création de l'app Flask: {e}")
        return False

def check_port_availability():
    """Vérifie la disponibilité des ports courants"""
    print_header("VÉRIFICATION DES PORTS")
    
    common_ports = [5000, 8000, 8080, 3000]
    
    import socket
    available_ports = []
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', port))
        sock.close()
        
        if result != 0:
            available_ports.append(port)
            print_success(f"Port {port}: Disponible")
        else:
            print_warning(f"Port {port}: Occupé")
    
    return available_ports

def get_pip_list():
    """Liste les packages installés"""
    print_header("PACKAGES INSTALLÉS")
    
    try:
        import pkg_resources
        packages = sorted([f"{pkg.key}=={pkg.version}" 
                          for pkg in pkg_resources.working_set])
        
        print_info(f"Nombre total de packages: {len(packages)}")
        
        # Afficher seulement les packages liés à Flask/web
        flask_related = [pkg for pkg in packages 
                        if any(keyword in pkg.lower() 
                              for keyword in ['flask', 'werkzeug', 'jinja', 'wsgi'])]
        
        for pkg in flask_related:
            print_info(f"  {pkg}")
        
        if len(packages) > 20:
            print_info("(Utilisez 'pip list' pour voir tous les packages)")
        
        return True
    except Exception as e:
        print_error(f"Impossible de lister les packages: {e}")
        return False

def main():
    """Fonction principale"""
    print("\n" + "="*60)
    print("   DIAGNOSTIC FLASK COMPLET")
    print("="*60)
    
    # Informations système
    print_info(f"Date du diagnostic: {datetime.now()}")
    print_info(f"Système: {sys.platform}")
    print_info(f"Répertoire courant: {os.getcwd()}")
    
    # Exécution des vérifications
    checks = [
        ("Version Python", check_python_version()),
        ("Installation Flask", check_flask_installation()),
        ("Dépendances Flask", check_flask_dependencies()),
        ("Environnement virtuel", check_virtual_environment()),
        ("Structure projet", check_project_structure()),
        ("Test application", test_flask_app()),
    ]
    
    # Vérifications supplémentaires (non bloquantes)
    check_port_availability()
    get_pip_list()
    
    # Résumé
    print_header("RÉSUMÉ")
    
    successful = sum(1 for _, result in checks if result)
    total = len(checks)
    
    print_info(f"Tests réussis: {successful}/{total}")
    
    if successful == total:
        print_success("✅ Environnement Flask prêt!")
    elif successful >= total * 0.7:
        print_warning("⚠️  Environnement Flask partiellement configuré")
    else:
        print_error("❌ Problèmes majeurs détectés")
    
    # Recommandations
    print_header("RECOMMANDATIONS")
    
    if not check_flask_installation():
        print("1. Installez Flask: pip install flask")
    
    if not check_virtual_environment():
        print("2. Créez un environnement virtuel: python -m venv venv")
    
    if not check_project_structure():
        print("3. Créez une structure de base: mkdir templates static")
    
    # Fin
    print("\n" + "="*60)
    print("Diagnostic terminé!")
    print("="*60)
    
    if sys.platform != "linux":
        input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrompu.")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erreur inattendue: {e}")
        sys.exit(1)
