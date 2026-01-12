# config.py
import os
from pathlib import Path

class Config:
    # Chemins
    BASE_DIR = Path(__file__).parent
    GENERATED_CODE_DIR = BASE_DIR / "generated_code"
    TEMPLATES_DIR = BASE_DIR / "templates"
    
    # Options de génération
    DEFAULT_COMPLEXITY = "simple"
    SUPPORTED_COMPLEXITIES = ["simple", "medium", "complex"]
    
    # Modèles disponibles
    CODE_TEMPLATES = {
        "simple": "Application Flask basique avec 2-3 routes",
        "api": "API REST avec endpoints CRUD",
        "form": "Application avec formulaires",
        "database": "Application avec base de données",
        "auth": "Système d'authentification"
    }
