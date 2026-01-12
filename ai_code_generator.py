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
