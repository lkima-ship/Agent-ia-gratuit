cat > /root/ai_agents_project/src/app.py << 'EOF'
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "AI Agents System",
        "status": "online",
        "port": 5002,
        "directory": os.getcwd()
    })

@app.route('/api/test')
def test():
    return jsonify({"test": "success", "timestamp": os.times()})

if __name__ == '__main__':
    print("Starting server on http://0.0.0.0:5002")
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
