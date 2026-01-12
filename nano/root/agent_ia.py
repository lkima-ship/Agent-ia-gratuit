from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

# Initialiser la base de données
def init_db():
    conn = sqlite3.connect('/root/knowledge.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge
                 (id INTEGER PRIMARY KEY, client_id TEXT, question TEXT, answer TEXT)''')
    conn.commit()
    conn.close()

init_db()

def search_knowledge_base(query, client_id):
    """Recherche dans la base de connaissances"""
    conn = sqlite3.connect('/root/knowledge.db')
    c = conn.cursor()
    c.execute("SELECT answer FROM knowledge WHERE client_id = ? AND question LIKE ?", 
              (client_id, f'%{query}%'))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def generate_ai_response(query, context=None):
    """Génère une réponse avec IA (version simple)"""
    # Pour l'instant, une réponse simple
    responses = {
        "bonjour": "Bonjour ! Comment puis-je vous aider ?",
        "prix": "Nos prix varient selon le service. Pouvez-vous préciser ?",
        "rdv": "Pour prendre rendez-vous, contactez-nous au 01 23 45 67 89."
    }
    
    query_lower = query.lower()
    for key, value in responses.items():
        if key in query_lower:
            return value
    
    return f"Je vais vous aider avec : '{query}'. Contactez-nous pour plus d'informations."

def log_conversation(client_id, query, answer):
    """Log la conversation"""
    conn = sqlite3.connect('/root/knowledge.db')
    c = conn.cursor()
    c.execute("INSERT INTO logs (client_id, query, answer, timestamp) VALUES (?, ?, ?, datetime('now'))",
              (client_id, query, answer))
    conn.commit()
    conn.close()

@app.route('/api/support', methods=['POST'])
def customer_support():
    """Endpoint pour le support client"""
    try:
        data = request.json
        query = data.get('question', '')
        client_id = data.get('client_id', 'default')
        
        # 1. Recherche dans base de connaissances
        answer = search_knowledge_base(query, client_id)
        
        # 2. Si pas trouvé, utiliser IA générative
        if not answer:
            answer = generate_ai_response(query)
        
        # 3. Logger pour amélioration
        log_conversation(client_id, query, answer)
        
        return jsonify({
            'answer': answer,
            'confidence': 0.8,
            'escalate_to_human': False
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return """
    <h1>Agent IA Multi-fonctions</h1>
    <p>Endpoints disponibles :</p>
    <ul>
        <li><code>POST /api/support</code> - Support client</li>
        <li><code>GET /api/status</code> - Statut du service</li>
    </ul>
    """

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'online',
        'service': 'Agent IA Multi-fonctions',
        'version': '1.0'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
