# Copier le script qui fonctionne
cp /root/test_flask.py /root/simple_working.py

# Ou modifier test_flask.py pour qu'il ressemble à l'original
cat > /root/simple_working.py << 'EOF'
from flask import Flask
import sys

app = Flask(__name__)

@app.route('/')
def home():
    print("DEBUG: Route / appelée", file=sys.stdout)
    return 'WORKING'

if __name__ == '__main__':
    print("DEBUG: Début de app.run()", file=sys.stderr)
    app.run(host='0.0.0.0', port=5002, debug=False)
EOF
