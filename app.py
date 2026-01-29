from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        "app": "Agent IA Gratuit",
        "status": "online",
        "timestamp": datetime.datetime.now().isoformat(),
        "endpoints": ["/", "/api/status", "/api/chat"]
    })

@app.route('/api/status')
def status():
    return jsonify({"status": "healthy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if data and 'message' in data:
        return jsonify({
            "response": f"Agent IA: {data['message']}",
            "timestamp": datetime.datetime.now().isoformat()
        })
    return jsonify({"error": "No message"}), 400

if __name__ == '__main__':
    app.run()
