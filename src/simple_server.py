# Supprimer le fichier existant s'il y a des erreurs
rm -f src/simple_server.py

# Créer un nouveau fichier ligne par ligne
echo "from http.server import HTTPServer, BaseHTTPRequestHandler" > src/simple_server.py
echo "" >> src/simple_server.py
echo "class Handler(BaseHTTPRequestHandler):" >> src/simple_server.py
echo "    def do_GET(self):" >> src/simple_server.py
echo "        self.send_response(200)" >> src/simple_server.py
echo "        self.send_header('Content-type', 'text/plain')" >> src/simple_server.py
echo "        self.end_headers()" >> src/simple_server.py
echo "        self.wfile.write(b'Hello from Agent IA Gratuit!')" >> src/simple_server.py
echo "" >> src/simple_server.py
echo "    def log_message(self, format, *args):" >> src/simple_server.py
echo "        print(f'Server: {args[0]} {args[1]}')" >> src/simple_server.py
echo "" >> src/simple_server.py
echo "print('Starting server on port 8000...')" >> src/simple_server.py
echo "print('Access: http://localhost:8000')" >> src/simple_server.py
echo "print('Press Ctrl+C to stop')" >> src/simple_server.py
echo "" >> src/simple_server.py
echo "server = HTTPServer(('0.0.0.0', 8000), Handler)" >> src/simple_server.py
echo "server.serve_forever()" >> src/simple_server.py
