# Vérifier le contenu actuel
cat /root/simple_working.py

# Si c'est vide ou erroné, le recréer
cat > /root/simple_working.py << 'EOF'
from flask import Flask
import sys
import time

app = Flask(__name__)

@app.route('/')
def home():
    print(f"[{time.ctime()}] Route / appelée", file=sys.stdout, flush=True)
    return 'WORKING'

if __name__ == '__main__':
    print(f"[{time.ctime()}] Démarrage de Flask sur le port 5002...", file=sys.stderr, flush=True)
    app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
EOF
