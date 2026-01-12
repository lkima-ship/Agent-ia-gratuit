#!/usr/bin/env python3
# ↑↑↑ Cette ligne est CRUCIALE pour Linux! (shebang)

import sys
import os
import subprocess
from pathlib import Path

# Vérifier la version de Python
if sys.version_info.major < 3:
    print("❌ ERREUR: Python 3 est requis!")
    print("⚠️  Utilisez 'python3 flask_doctor.py' au lieu de 'python'")
    sys.exit(1)

# Vérifier les dépendances
def check_dependencies():
    """Vérifie que Flask est installé"""
    try:
        import flask
        return True
    except ImportError:
        return False
