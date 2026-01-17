cat > /root/web_interface.py << 'EOF'
#!/usr/bin/env python3
"""
INTERFACE WEB LÉGÈRE POUR AGENTS IA
Serveur minimaliste avec HTML/JS intégré
"""
import http.server
import socketserver
import json
import threading
from urllib.parse import parse_qs, urlparse
import os

class AgentWebHandler(http.server.SimpleHTTPRequestHandler):
    """Gestionnaire HTTP personnalisé"""
    
    agents_disponibles = {
        "cognitive": "/root/agent_cognitif.py",
        "web": "/root/agent_web_avance_v2.py",
        "plugins": "/root/plugin_manager.py",
        "surveillance": "/root/agent_surveillance.py"
    }
    
    def do_GET(self):
        """Gère les requêtes GET"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self._serve_html()
        elif parsed_path.path == '/agents':
            self._list_agents()
        elif parsed_path.path == '/status':
            self._system_status()
        else:
            self.send_error(404, "Ressource non trouvée")
    
    def do_POST(self):
        """Gère les requêtes POST"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(post_data)
            action = data.get('action', '')
            
            if action == 'execute_agent':
                agent = data.get('agent', '')
                params = data.get('params', {})
                result = self._execute_agent(agent, params)
                self._send_json_response(result)
            else:
                self._send_json_response({"error": "Action non reconnue"})
        except Exception as e:
            self._send_json_response({"error": str(e)})
    
    def _serve_html(self):
        """Sert l'interface HTML"""
        html_content = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Agents IA - Interface Web</title>
            <style>
                body {
                    font-family: 'Segoe UI', Arial, sans-serif;
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 30px;
                    margin: 20px 0;
                }
                .agent-card {
                    background: rgba(255, 255, 255, 0.2);
                    border-radius: 10px;
                    padding: 20px;
                    margin: 15px 0;
                    cursor: pointer;
                    transition: transform 0.3s;
                }
                .agent-card:hover {
                    transform: translateY(-5px);
                    background: rgba(255, 255, 255, 0.3);
                }
                .btn {
                    background: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 5px;
                    cursor: pointer;
                    margin: 5px;
                }
                .output {
                    background: rgba(0, 0, 0, 0.3);
                    border-radius: 10px;
                    padding: 15px;
                    margin: 15px 0;
                    font-family: monospace;
                    max-height: 300px;
                    overflow-y: auto;
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .status {
                    display: inline-block;
                    padding: 5px 10px;
                    border-radius: 15px;
                    font-size: 12px;
                    margin-left: 10px;
                }
                .online { background: #4CAF50; }
                .offline { background: #f44336; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 Système d'Agents IA Intelligent</h1>
                <p>Interface web légère pour contrôler vos agents IA</p>
                
                <div id="systemStatus" class="agent-card">
                    <h3>📊 État du système</h3>
                    <div id="statusDetails"></div>
                </div>
                
                <div class="agent-card" onclick="executeAgent('cognitive')">
                    <h3>🧠 Agent Cognitif <span id="cognitiveStatus" class="status">...</span></h3>
                    <p>IA avec mémoire et prise de décision</p>
                    <input type="text" id="cognitiveInput" placeholder="Votre requête..." style="width: 80%; padding: 10px; border-radius: 5px; border: none; margin-top: 10px;">
                    <button class="btn" onclick="executeAgent('cognitive')">Exécuter</button>
                </div>
                
                <div class="agent-card" onclick="executeAgent('web')">
                    <h3>🌐 Agent Web Avancé <span id="webStatus" class="status">...</span></h3>
                    <p>Scraping, analyse SEO, surveillance</p>
                    <input type="text" id="webInput" placeholder="URL à analyser..." style="width: 80%; padding: 10px; border-radius: 5px; border: none; margin-top: 10px;">
                    <button class="btn" onclick="executeAgent('web')">Analyser</button>
                </div>
                
                <div class="agent-card" onclick="executeAgent('plugins')">
                    <h3>🧩 Gestionnaire de Plugins <span id="pluginsStatus" class="status">...</span></h3>
                    <p>Système extensible de plugins</p>
                    <button class="btn" onclick="executeAgent('plugins')">Ouvrir</button>
                </div>
                
                <div class="output" id="output">
                    <h4>📝 Sortie des agents :</h4>
                    <div id="outputContent">En attente d'exécution...</div>
                </div>
            </div>
            
            <script>
                // Mettre à jour le statut
                function updateStatus() {
                    fetch('/status')
                        .then(r => r.json())
                        .then(data => {
                            document.getElementById('statusDetails').innerHTML = 
                                `CPU: ${data.cpu}% | RAM: ${data.ram}% | Agents: ${data.agents}`;
                            
                            // Mettre à jour les statuts des agents
                            data.agents_status.forEach(agent => {
                                const elem = document.getElementById(agent.name + 'Status');
                                if (elem) {
                                    elem.textContent = agent.status ? '✅ Online' : '❌ Offline';
                                    elem.className = 'status ' + (agent.status ? 'online' : 'offline');
                                }
                            });
                        });
                }
                
                // Exécuter un agent
                function executeAgent(agentName) {
                    let inputElem = document.getElementById(agentName + 'Input');
                    let inputValue = inputElem ? inputElem.value : '';
                    
                    fetch('/agents', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            action: 'execute_agent',
                            agent: agentName,
                            params: {input: inputValue}
                        })
                    })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('outputContent').innerHTML = 
                            `<pre>${JSON.stringify(data, null, 2)}</pre>`;
                        
                        if (inputElem) inputElem.value = '';
                    });
                }
                
                // Actualiser périodiquement
                setInterval(updateStatus, 5000);
                updateStatus(); // Premier appel
                
                // Exemple de commandes rapides
                const quickCommands = [
                    {cmd: "Analyse SEO de google.com", agent: "web"},
                    {cmd: "Statistiques système", agent: "cognitive"},
                    {cmd: "Lister les plugins", agent: "plugins"}
                ];
                
                // Ajouter les commandes rapides
                quickCommands.forEach(cmd => {
                    const btn = document.createElement('button');
                    btn.className = 'btn';
                    btn.textContent = cmd.cmd;
                    btn.onclick = () => {
                        document.getElementById(cmd.agent + 'Input').value = cmd.cmd.split(' ')[2] || '';
                        executeAgent(cmd.agent);
                    };
                    document.querySelector('.container').appendChild(btn);
                });
            </script>
        </body>
        </html>
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))
    
    def _list_agents(self):
        """Liste les agents disponibles"""
        agents = []
        for name, path in self.agents_disponibles.items():
            agents.append({
                "name": name,
                "path": path,
                "exists": os.path.exists(path)
            })
        
        self._send_json_response({"agents": agents})
    
    def _system_status(self):
        """Retourne le statut du système"""
        import psutil
        
        status = {
            "cpu": psutil.cpu_percent(),
            "ram": psutil.virtual_memory().percent,
            "agents": len(self.agents_disponibles),
            "agents_status": []
        }
        
        for name, path in self.agents_disponibles.items():
            status["agents_status"].append({
                "name": name,
                "status": os.path.exists(path)
            })
        
        self._send_json_response(status)
    
    def _execute_agent(self, agent_name, params):
        """Exécute un agent"""
        if agent_name in self.agents_disponibles:
            path = self.agents_disponibles[agent_name]
            if os.path.exists(path):
                # Simulation d'exécution (dans la vraie version, on exécuterait réellement l'agent)
                return {
                    "agent": agent_name,
                    "status": "executed",
                    "params": params,
                    "output": f"Agent {agent_name} exécuté avec succès",
                    "timestamp": json.dumps(str(threading.current_thread().ident))
                }
        
        return {"error": f"Agent {agent_name} non trouvé"}
    
    def _send_json_response(self, data):
        """Envoie une réponse JSON"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def demarrer_serveur(port=8080):
    """Démarre le serveur web"""
    handler = AgentWebHandler
    
    # Créer le répertoire pour les ressources statiques
    os.makedirs("/root/static", exist_ok=True)
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🌐 Serveur web démarré sur http://localhost:{port}")
        print(f"📁 Interface disponible : http://localhost:{port}")
        print("📱 Accessible depuis n'importe quel navigateur")
        print("\n📊 Agents accessibles :")
        print("  • Agent Cognitif : /cognitive")
        print("  • Agent Web : /web")
        print("  • Plugins : /plugins")
        print("\n🛑 Pour arrêter : Ctrl+C")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Serveur arrêté")
            httpd.server_close()

if __name__ == "__main__":
    demarrer_serveur()
EOF
