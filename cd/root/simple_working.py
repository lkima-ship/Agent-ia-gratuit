# Créer une version améliorée du script Flask
cat > /root/simple_working.py << 'EOF'
from flask import Flask
import sys
import time

app = Flask(__name__)

@app.route('/')
def home():
    print(f"[{time.time()}] Route / appelée", file=sys.stdout, flush=True)
    return 'WORKING'

if __name__ == '__main__':
    print(f"[{time.time()}] Démarrage de Flask...", file=sys.stderr, flush=True)
    try:
        app.run(host='0.0.0.0', port=5002, debug=False, threaded=True)
    except Exception as e:
        print(f"[{time.time()}] Erreur: {e}", file=sys.stderr, flush=True)
EOF
