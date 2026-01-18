# Créer un test Python simple
cat > /root/test_simple.py << 'EOF'
import socket
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

if __name__ == '__main__':
    # Vérifier que le port est libre
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 5002))
    if result == 0:
        print("Port 5002 déjà utilisé!")
    else:
        print("Port 5002 libre, démarrage...")
        app.run(host='0.0.0.0', port=5002)
EOF

# Exécuter
python3 /root/test_simple.py
