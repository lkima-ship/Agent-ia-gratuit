# ia_agent.py
import os
import json
from datetime import datetime
from pathlib import Path

class FlaskCodeGenerator:
    """Générateur de code Flask intelligent"""
    
    def __init__(self):
        self.templates_dir = Path("templates")
        self.generated_dir = Path("generated_code")
        self._setup_directories()
        
    def _setup_directories(self):
        """Crée les répertoires nécessaires"""
        self.templates_dir.mkdir(exist_ok=True)
        self.generated_dir.mkdir(exist_ok=True)
    
    def generate_from_description(self, description, complexity="simple"):
        """Génère du code Flask basé sur une description"""
        # Si vous avez accès à OpenAI, intégrez-le ici
        # Sinon, utilisez un système de templates intelligent
        
        template = self._select_template(description, complexity)
        code = self._fill_template(template, description)
        
        return {
            "success": True,
            "code": code,
            "template_used": template["name"]
        }
    
    def _select_template(self, description, complexity):
        """Sélectionne un template approprié basé sur la description"""
        templates = {
            "simple": self._get_simple_template(),
            "api": self._get_api_template(),
            "form": self._get_form_template(),
            "database": self._get_database_template(),
            "auth": self._get_auth_template()
        }
        
        # Analyse simple de la description pour choisir le template
        desc_lower = description.lower()
        
        if "api" in desc_lower or "json" in desc_lower:
            return templates["api"]
        elif "form" in desc_lower or "formulaire" in desc_lower:
            return templates["form"]
        elif "base" in desc_lower or "donnée" in desc_lower or "db" in desc_lower:
            return templates["database"]
        elif "auth" in desc_lower or "login" in desc_lower or "connexion" in desc_lower:
            return templates["auth"]
        else:
            return templates["simple"]
    
    def _get_simple_template(self):
        return {
            "name": "simple",
            "code": '''from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    """Page d'accueil"""
    return "<h1>Bienvenue sur mon application Flask!</h1>"

@app.route('/about')
def about():
    """Page À propos"""
    return "<p>Cette application a été générée avec Flask Doctor</p>"

if __name__ == '__main__':
    app.run(debug=True)
'''
        }
    
    def _get_api_template(self):
        return {
            "name": "api",
            "code": '''from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Active CORS pour l'API

# Données exemple
items = [
    {"id": 1, "name": "Item 1", "description": "Premier item"},
    {"id": 2, "name": "Item 2", "description": "Deuxième item"}
]

@app.route('/api/items', methods=['GET'])
def get_items():
    """Récupère tous les items"""
    return jsonify({"items": items, "count": len(items)})

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Récupère un item par son ID"""
    item = next((i for i in items if i["id"] == item_id), None)
    if item:
        return jsonify(item)
    return jsonify({"error": "Item non trouvé"}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    """Crée un nouvel item"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données JSON requises"}), 400
    
    new_id = max([i["id"] for i in items], default=0) + 1
    new_item = {
        "id": new_id,
        "name": data.get("name", ""),
        "description": data.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
'''
        }
    
    def _fill_template(self, template, description):
        """Personnalise le template avec la description"""
        code = template["code"]
        
        # Ajoute un commentaire avec la description
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = f'''"""
Application Flask générée par Flask Doctor
Description: {description}
Date de génération: {timestamp}
"""
'''
        
        return header + code
    
    def save_code(self, code, project_name):
        """Sauvegarde le code dans un fichier"""
        filename = f"{project_name.replace(' ', '_').lower()}.py"
        filepath = self.generated_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(code)
        
        return filepath
    
    def create_html_template(self, project_name):
        """Crée un template HTML basique"""
        html_content = f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {{ padding-top: 20px; background-color: #f8f9fa; }}
        .container {{ max-width: 960px; }}
        .generated-info {{ background-color: #e9ecef; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="generated-info">
            <h1>Application Flask: {project_name}</h1>
            <p>Généré automatiquement par Flask Doctor</p>
            <small>Date: {datetime.now().strftime("%Y-%m-%d")}</small>
        </div>
        
        <div class="card">
            <div class="card-body">
                <h2 class="card-title">Fonctionnalités</h2>
                <ul>
                    <li>Application Flask prête à l'emploi</li>
                    <li>Structure organisée</li>
                    <li>Code commenté en français</li>
                    <li>Responsive avec Bootstrap</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
'''
        
        html_path = self.templates_dir / "index.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_path
