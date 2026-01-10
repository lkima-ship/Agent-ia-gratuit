cat > src/simple_server.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        response = "🤖 Agent IA Gratuit - Serveur actif!\n"
        response += "Version: 1.0.0\n"
        response += "Endpoint: /\n"
        self.wfile.write(response.encode())
    
    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    print("=" * 50)
    print("🤖 Agent IA Gratuit - Serveur Web")
    print("=" * 50)
    print("🚀 Démarrage sur le port 8000...")
    print("📡 Accédez à: http://localhost:8000")
    print("🛑 Arrêter avec: Ctrl+C")
    print("=" * 50)
    
    server = HTTPServer(('0.0.0.0', 8000), SimpleHandler)
    server.serve_forever()
EOF
