cat > src/simple_server.py << 'EOF'
"""
Serveur web simple sans dépendances externes
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Agent IA Gratuit - Serveur simple",
                "status": "running",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        elif self.path == '/info':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            info = {
                "name": "Agent IA Gratuit",
                "version": "1.0.0",
                "description": "Assistant IA intelligent",
                "endpoints": ["/", "/health", "/info"]
            }
            self.wfile.write(json.dumps(info).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found", "path": self.path}).encode())
    
    def log_message(self, format, *args):
        # Réduire les logs pour la console
        pass

def run_server(port=8000):
    print("🚀 Agent IA Gratuit - Serveur web")
    print("=" * 40)
    print(f"📡 Accédez à: http://localhost:{port}")
    print(f"❤️  Santé: http://localhost:{port}/health")
    print(f"📋 Info: http://localhost:{port}/info")
    print("🛑 Pour arrêter: Ctrl+C")
    print("=" * 40)
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Serveur arrêté proprement")

if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Usage: {sys.argv[0]} [port]")
            sys.exit(1)
    
    run_server(port)
EOF
