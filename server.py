echo 'import http.server' > server.py
echo 'import socketserver' >> server.py
echo '' >> server.py
echo 'PORT = 8000' >> server.py
echo '' >> server.py
echo 'class MyHandler(http.server.BaseHTTPRequestHandler):' >> server.py
echo '    def do_GET(self):' >> server.py
echo '        self.send_response(200)' >> server.py
echo '        self.send_header("Content-type", "text/plain")' >> server.py
echo '        self.end_headers()' >> server.py
echo '        self.wfile.write(b"Agent IA Gratuit - Serveur fonctionnel!")' >> server.py
echo '' >> server.py
echo 'print("🤖 Agent IA Gratuit - Serveur Web")' >> server.py
echo 'print("================================")' >> server.py
echo 'print(f"🚀 Port: {PORT}")' >> server.py
echo 'print(f"📡 URL: http://localhost:{PORT}")' >> server.py
echo 'print("🛑 Ctrl+C pour arrêter")' >> server.py
echo '' >> server.py
echo 'with socketserver.TCPServer(("", PORT), MyHandler) as httpd:' >> server.py
echo '    httpd.serve_forever()' >> server.py
