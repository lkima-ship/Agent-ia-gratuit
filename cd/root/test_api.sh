# Si rien ne fonctionne, créer un script de test ultra-simple
cat > /root/test_api.sh << 'EOF'
#!/bin/sh
echo "🔧 Test API Flask"
pkill -f python 2>/dev/null
echo "1. Démarrage..."
python3 -c "
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return 'TEST OK'
import threading
thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5002, debug=False))
thread.daemon = True
thread.start()
import time
time.sleep(3)
" &
sleep 3
echo "2. Test..."
curl -s http://localhost:5002 && echo " ✅" || echo " ❌"
EOF

chmod +x /root/test_api.sh
./root/test_api.sh
