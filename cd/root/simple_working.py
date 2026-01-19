# Recréer un script Flask simple qui fonctionne
cat > /root/simple_working.py << 'EOF'
from flask import Flask
import sys
import time
import os

app = Flask(__name__)

@app.route('/')
def home():
    print(f"[{time.strftime('%H:%M:%S')}] Route / appelée", file=sys.stdout, flush=True)
    return 'API FONCTIONNE!'

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    print(f"[{time.strftime('%H:%M:%S')}] Démarrage de Flask...", file=sys.stderr, flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] PID: {os.getpid()}", file=sys.stderr, flush=True)
    print(f"[{time.strftime('%H:%M:%S')}] Port: 5002", file=sys.stderr, flush=True)
    
    try:
        app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERREUR: {e}", file=sys.stderr, flush=True)
EOF
