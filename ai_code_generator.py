cat > ~/ai_code_generator.py << 'EOF'
#!/usr/bin/env python3
"""
Agent IA qui génère du code Flask basé sur des descriptions
"""

class FlaskCodeGenerator:
    def __init__(self):
        self.templates = {
            'basic': self.basic_app,
            'api': self.api_app,
            'crud': self.crud_app,
        }
    
    def basic_app(self):
        return '''from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
'''
    
    def api_app(self):
        return '''from flask import Flask, jsonify, request
app = Flask(__name__)

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({"data": "example"})

@app.route('/api/data', methods=['POST'])
def post_data():
    data = request.json
    return jsonify({"received": data})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
'''
    
    def crud_app(self):
        return '''from flask import Flask, request, jsonify
app = Flask(__name__)

items = []

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def create_item():
    item = request.json
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    if 0 <= id < len(items):
        items[id] = request.json
        return jsonify(items[id])
    return jsonify({"error": "Not found"}), 404

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    if 0 <= id < len(items):
        return jsonify(items.pop(id))
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
'''
    
    def generate(self, app_type='basic'):
        """Génère une application Flask"""
        if app_type in self.templates:
            return self.templates[app_type]()
        else:
            return "Invalid app type"

def main():
    """Interface interactive pour générer du code"""
    print("🤖 Flask Code Generator")
    print("=" * 40)
    
    generator = FlaskCodeGenerator()
    
    print("Select app type:")
    print("1. Basic Flask App")
    print("2. REST API")
    print("3. CRUD Application")
    
    choice = input("\nChoice (1-3): ").strip()
    
    types = {'1': 'basic', '2': 'api', '3': 'crud'}
    
    if choice in types:
        app_type = types[choice]
        code = generator.generate(app_type)
        
        filename = f"generated_{app_type}_app.py"
        with open(filename, 'w') as f:
            f.write(code)
            
        print(f"\n✅ Generated {filename}")
        print(f"👉 Run with: python3 {filename}")
        
        # Aperçu
        print("\n📝 Preview (first 15 lines):")
        print("-" * 30)
        lines = code.split('\n')[:15]
        for line in lines:
            print(line)
        if len(code.split('\n')) > 15:
            print("...")
        print("-" * 30)
    else:
        print("❌ Invalid choice")

if __name__ == '__main__':
    main()
EOF
# MODIFIEZ VOTRE FICHIER EXISTANT flask_doctor.py

# Ajoutez ces imports au début du fichier
from ia_agent import FlaskCodeGenerator
from pathlib import Path
import subprocess
import sys
import os

# MODIFIEZ la fonction ai_code_generator() dans votre menu :
def ai_code_generator():
    """Générateur de code IA amélioré"""
    print("\n=== AI Code Generator ===")
    print("Générateur de code basé sur l'IA")
    
    # Initialiser le générateur
    generator = FlaskCodeGenerator()
    
    # Demander la description
    description = input("\nDescription du code à générer : ")
    
    # Demander le type d'application
    print("\nTypes d'application disponibles :")
    print("1. Simple (routes basiques)")
    print("2. API REST")
    print("3. Avec formulaires")
    print("4. Avec base de données")
    print("5. Avec authentification")
    
    choice = input("\nChoisissez le type (1-5) [1]: ") or "1"
    
    type_map = {
        "1": "simple",
        "2": "api",
        "3": "form",
        "4": "database",
        "5": "auth"
    }
    
    app_type = type_map.get(choice, "simple")
    
    # Demander le nom du projet
    project_name = input("\nNom du projet [mon_app_flask]: ") or "mon_app_flask"
    
    print("\n⏳ Génération du code en cours...")
    
    # Générer le code
    result = generator.generate_from_description(description, app_type)
    
    if result["success"]:
        # Sauvegarder le code
        filepath = generator.save_code(result["code"], project_name)
        
        # Créer un template HTML
        generator.create_html_template(project_name)
        
        print("\n" + "="*60)
        print("✅ CODE GÉNÉRÉ AVEC SUCCÈS !")
        print("="*60)
        
        # Afficher un aperçu du code
        print(f"\nFichier généré : {filepath}")
        print(f"Type d'application : {result['template_used']}")
        
        # Afficher les premières lignes du code
        print("\n--- Aperçu du code ---")
        lines = result["code"].split('\n')[:15]
        for line in lines:
            print(line)
        
        print("\n--- Instructions ---")
        print(f"1. Pour exécuter : python {filepath}")
        print(f"2. Accédez à : http://localhost:5000")
        print(f"3. Fichier HTML généré dans : templates/index.html")
        
        # Options supplémentaires
        print("\nOptions :")
        print("1. Exécuter l'application maintenant")
        print("2. Voir le code complet")
        print("3. Retour au menu")
        
        option = input("\nVotre choix (1-3) [3]: ") or "3"
        
        if option == "1":
            run_flask_app(filepath)
        elif option == "2":
            print("\n" + "="*60)
            print(result["code"])
            print("="*60)
    
    else:
        print("\n❌ Erreur lors de la génération du code")
        print(result.get("error", "Erreur inconnue"))

def run_flask_app(filepath):
    """Exécute l'application Flask générée"""
    print(f"\n🚀 Lancement de l'application...")
    print(f"📂 Fichier : {filepath}")
    print("\n📋 Informations :")
    print("- Serveur accessible à : http://localhost:5000")
    print("- Appuyez sur Ctrl+C pour arrêter")
    print("- Vérifiez les logs Flask ci-dessous")
    print("\n" + "="*60)
    
    try:
        # Définir les variables d'environnement Flask
        os.environ['FLASK_APP'] = str(filepath)
        os.environ['FLASK_ENV'] = 'development'
        
        # Lancer Flask
        subprocess.run([sys.executable, "-m", "flask", "run"], check=True)
    except KeyboardInterrupt:
        print("\n\n⏹️ Application arrêtée par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement : {e}")
    
