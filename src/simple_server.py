cat > src/simple_server.py << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "message": "Agent IA Gratuit",
                "status": "running",
                "version": "1.0.0"
            }
            self.wfile.write(json.dumps(response).encode())
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "healthy"}).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())
    
    def log_message(self, format, *args):
        # Réduire les logs
        pass

def run_server(port=8000):
    print("🚀 Serveur web Agent IA Gratuit démarré")
    print(f"📡 Adresse: http://localhost:{port}")
    print("🛑 Pour arrêter: Ctrl+C")
    print("----------------------------------------")
    
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n✅ Serveur arrêté proprement")

if __name__ == "__main__":
    run_server()
EOF
