echo 'import http.server' > server.py
echo 'import socketserver' >> server.py
echo '' >> server.py
echo 'PORT = 8000' >> server.py
echo '' >> server.py
echo 'class Handler(http.server.BaseHTTPRequestHandler):' >> server.py
echo '    def do_GET(self):' >> server.py
echo '        self.send_response(200)' >> server.py
echo '        self.send_header("Content-type", "text/plain")' >> server.py
echo '        self.end_headers()' >> server.py
echo '        self.wfile.write(b"Hello from Agent IA Gratuit Server!")' >> server.py
echo '' >> server.py
echo 'print("Starting server...")' >> server.py
echo 'print("Port: 8000")' >> server.py
echo 'print("URL: http://localhost:8000")' >> server.py
echo 'print("Stop: Ctrl+C")' >> server.py
echo '' >> server.py
echo 'httpd = socketserver.TCPServer(("", PORT), Handler)' >> server.py
echo 'httpd.serve_forever()' >> server.py
