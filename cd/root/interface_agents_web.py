# Créer une interface web améliorée
cat > /root/interface_agents_web.py << 'EOF'
#!/usr/bin/env python3
"""
🌐 INTERFACE WEB UNIFIÉE - Tous les agents
Serveur web avec détection automatique et lancement
"""
import http.server
import socketserver
import json
import os
import sys
import subprocess
import threading
import time
from datetime import datetime
import webbrowser

PORT = 8080

class AgentWebHandler(http.server.BaseHTTPRequestHandler):
    """Gestionnaire HTTP avec interface web complète"""
    
    agents_cache = []
    last_scan = None
    
    @classmethod
    def scan_agents(cls):
        """Scan les agents disponibles"""
        cls.last_scan = datetime.now()
        cls.agents_cache = []
        
        agents_dir = "/root"
        for file in os.listdir(agents_dir):
            if file.endswith(".py"):
                filepath = os.path.join(agents_dir, file)
                
                # Lire les premières lignes pour détecter le type
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(200).lower()
                    
                    # Déterminer la catégorie
                    category = "general"
                    categories = {
                        "web": ["web", "interface", "http"],
                        "ia": ["ia", "intelligence", "cognitif", "ml"],
                        "analyse": ["analyse", "data", "stats"],
                        "system": ["system", "surveillance", "monitor"],
                        "menu": ["menu", "principal", "hub"]
                    }
                    
                    for cat, keywords in categories.items():
                        if any(k in content or k in file.lower() for k in keywords):
                            category = cat
                            break
                    
                    # Statut
                    status = "active" if os.access(filepath, os.X_OK) else "inactive"
                    
                    # Description
                    description = "Agent Python"
                    if "web" in file.lower():
                        description = "Interface web"
                    elif "ia" in file.lower():
                        description = "Intelligence artificielle"
                    elif "analyse" in file.lower():
                        description = "Analyse de données"
                    
                    cls.agents_cache.append({
                        "id": len(cls.agents_cache),
                        "name": file,
                        "display_name": file.replace(".py", "").replace("_", " ").title(),
                        "path": filepath,
                        "category": category,
                        "status": status,
                        "description": description,
                        "size": os.path.getsize(filepath),
                        "last_modified": os.path.getmtime(filepath)
                    })
                except:
                    continue
        
        # Trier par catégorie puis nom
        cls.agents_cache.sort(key=lambda x: (x["category"], x["name"]))
    
    def do_GET(self):
        """Gère les requêtes GET"""
        path = self.path.split('?')[0]
        
        if path == '/':
            self.send_html_interface()
        elif path == '/api/agents':
            self.send_json_agents()
        elif path == '/api/status':
            self.send_system_status()
        elif path == '/api/categories':
            self.send_categories()
        elif path.startswith('/api/execute/'):
            agent_id = path.split('/')[-1]
            self.execute_agent(agent_id)
        elif path == '/style.css':
            self.send_css()
        elif path == '/script.js':
            self.send_javascript()
        else:
            self.send_error(404, "Ressource non trouvée")
    
    def do_POST(self):
        """Gère les requêtes POST"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            action = data.get('action')
            
            if action == 'scan':
                self.scan_agents()
                self.send_json({"success": True, "message": f"{len(self.agents_cache)} agents détectés"})
            elif action == 'execute':
                agent_name = data.get('agent')
                if agent_name:
                    self.execute_agent_by_name(agent_name)
                else:
                    self.send_json({"error": "Nom d'agent manquant"})
            else:
                self.send_json({"error": "Action non reconnue"})
        except Exception as e:
            self.send_json({"error": str(e)})
    
    def send_html_interface(self):
        """Envoie l'interface HTML"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🌐 Interface Web - Agents IA</title>
            <link rel="stylesheet" href="/style.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        </head>
        <body>
            <div class="container">
                <header>
                    <h1><i class="fas fa-robot"></i> Système d'Agents IA</h1>
                    <p>Interface web unifiée - Alpine Linux</p>
                    <div class="stats">
                        <span id="agentCount">...</span> agents disponibles
                    </div>
                </header>
                
                <div class="dashboard">
                    <div class="sidebar">
                        <div class="category-filter">
                            <h3><i class="fas fa-filter"></i> Catégories</h3>
                            <div id="categories"></div>
                        </div>
                        <div class="actions">
                            <h3><i class="fas fa-bolt"></i> Actions rapides</h3>
                            <button onclick="scanAgents()" class="btn btn-primary">
                                <i class="fas fa-sync"></i> Scanner agents
                            </button>
                            <button onclick="showAll()" class="btn btn-secondary">
                                <i class="fas fa-eye"></i> Tout voir
                            </button>
                            <button onclick="showSystem()" class="btn btn-info">
                                <i class="fas fa-server"></i> Système
                            </button>
                        </div>
                        <div class="system-info">
                            <h3><i class="fas fa-info-circle"></i> Infos système</h3>
                            <div id="systemInfo">Chargement...</div>
                        </div>
                    </div>
                    
                    <div class="main-content">
                        <div class="toolbar">
                            <div class="search">
                                <input type="text" id="searchInput" placeholder="Rechercher un agent...">
                                <button onclick="searchAgents()"><i class="fas fa-search"></i></button>
                            </div>
                            <div class="view-controls">
                                <button onclick="setView('grid')" class="view-btn active">
                                    <i class="fas fa-th"></i>
                                </button>
                                <button onclick="setView('list')" class="view-btn">
                                    <i class="fas fa-list"></i>
                                </button>
                            </div>
                        </div>
                        
                        <div class="agents-container">
                            <div id="agentsGrid" class="agents-grid"></div>
                            <div id="agentsList" class="agents-list" style="display: none;"></div>
                        </div>
                        
                        <div class="output-panel">
                            <h3><i class="fas fa-terminal"></i> Sortie des agents</h3>
                            <div id="output" class="output">
                                <div class="output-header">
                                    <span>Terminal</span>
                                    <button onclick="clearOutput()" class="btn-small">
                                        <i class="fas fa-trash"></i> Effacer
                                    </button>
                                </div>
                                <div id="outputContent" class="output-content">
                                    > Interface web initialisée. Prêt à contrôler les agents.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <footer>
                    <p>Système IA Alpine | <span id="currentTime"></span> | Agents actifs: <span id="activeAgents">0</span></p>
                </footer>
            </div>
            
            <script src="/script.js"></script>
            <script>
                // Mettre à jour l'heure
                function updateTime() {
                    const now = new Date();
                    document.getElementById('currentTime').textContent = 
                        now.toLocaleTimeString('fr-FR');
                }
                setInterval(updateTime, 1000);
                updateTime();
                
                // Charger initial
                loadAgents();
                loadSystemInfo();
                loadCategories();
            </script>
        </body>
        </html>
        """
        self.wfile.write(html.encode('utf-8'))
    
    def send_css(self):
        """Envoie le CSS"""
        self.send_response(200)
        self.send_header('Content-type', 'text/css')
        self.end_headers()
        
        css = """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            color: #7f8c8d;
            font-size: 1.1em;
        }
        
        .stats {
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            margin-top: 15px;
            font-weight: bold;
        }
        
        .dashboard {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .sidebar {
            flex: 1;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .main-content {
            flex: 3;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .category-filter, .actions, .system-info {
            margin-bottom: 25px;
        }
        
        h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .btn {
            display: block;
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            margin-bottom: 10px;
            transition: all 0.3s;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .btn-primary {
            background: #3498db;
            color: white;
        }
        
        .btn-secondary {
            background: #95a5a6;
            color: white;
        }
        
        .btn-info {
            background: #9b59b6;
            color: white;
        }
        
        .btn-success {
            background: #2ecc71;
            color: white;
        }
        
        .btn-warning {
            background: #f39c12;
            color: white;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .btn-small {
            padding: 6px 12px;
            font-size: 12px;
        }
        
        .toolbar {
            background: rgba(255, 255, 255, 0.95);
            padding: 15px 20px;
            border-radius: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .search {
            display: flex;
            flex: 1;
            max-width: 400px;
        }
        
        .search input {
            flex: 1;
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 8px 0 0 8px;
            font-size: 14px;
        }
        
        .search button {
            background: #3498db;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 0 8px 8px 0;
            cursor: pointer;
        }
        
        .view-controls {
            display: flex;
            gap: 10px;
        }
        
        .view-btn {
            background: #ecf0f1;
            border: none;
            padding: 10px;
            border-radius: 8px;
            cursor: pointer;
            color: #7f8c8d;
        }
        
        .view-btn.active {
            background: #3498db;
            color: white;
        }
        
        .agents-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            flex: 1;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
            overflow-y: auto;
            max-height: 500px;
        }
        
        .agents-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 20px;
        }
        
        .agent-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            border-left: 5px solid #3498db;
            transition: all 0.3s;
            cursor: pointer;
        }
        
        .agent-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.12);
        }
        
        .agent-card.web { border-left-color: #3498db; }
        .agent-card.ia { border-left-color: #2ecc71; }
        .agent-card.analyse { border-left-color: #9b59b6; }
        .agent-card.system { border-left-color: #f39c12; }
        .agent-card.menu { border-left-color: #e74c3c; }
        .agent-card.general { border-left-color: #95a5a6; }
        
        .agent-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .agent-name {
            font-weight: 600;
            color: #2c3e50;
            font-size: 16px;
        }
        
        .agent-status {
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }
        
        .status-active { background: #d5f4e6; color: #27ae60; }
        .status-inactive { background: #ffeaa7; color: #e67e22; }
        
        .agent-description {
            color: #7f8c8d;
            font-size: 13px;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        
        .agent-meta {
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #95a5a6;
        }
        
        .output-panel {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        }
        
        .output {
            background: #2c3e50;
            color: #ecf0f1;
            border-radius: 8px;
            margin-top: 10px;
            overflow: hidden;
        }
        
        .output-header {
            background: #34495e;
            padding: 10px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .output-content {
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }
        
        .category-item {
            display: flex;
            align-items: center;
            padding: 8px 12px;
            margin-bottom: 5px;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .category-item:hover {
            background: #ecf0f1;
        }
        
        .category-count {
            margin-left: auto;
            background: #bdc3c7;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
        }
        
        footer {
            text-align: center;
            color: white;
            padding: 20px;
            font-size: 14px;
        }
        
        @media (max-width: 1024px) {
            .dashboard {
                flex-direction: column;
            }
            
            .agents-grid {
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            }
        }
        
        @media (max-width: 768px) {
            .agents-grid {
                grid-template-columns: 1fr;
            }
        }
        """
        self.wfile.write(css.encode('utf-8'))
    
    def send_javascript(self):
        """Envoie le JavaScript"""
        self.send_response(200)
        self.send_header('Content-type', 'application/javascript')
        self.end_headers()
        
        js = """
        // Variables globales
        let currentView = 'grid';
        let currentCategory = 'all';
        let agents = [];
        
        // Charger les agents
        async function loadAgents() {
            try {
                const response = await fetch('/api/agents');
                agents = await response.json();
                displayAgents();
                updateStats();
            } catch (error) {
                console.error('Erreur:', error);
                addOutput('❌ Erreur de chargement des agents: ' + error.message);
            }
        }
        
        // Charger les catégories
        async function loadCategories() {
            try {
                const response = await fetch('/api/categories');
                const categories = await response.json();
                displayCategories(categories);
            } catch (error) {
                console.error('Erreur catégories:', error);
            }
        }
        
        // Charger les infos système
        async function loadSystemInfo() {
            try {
                const response = await fetch('/api/status');
                const systemInfo = await response.json();
                displaySystemInfo(systemInfo);
            } catch (error) {
                console.error('Erreur système:', error);
            }
        }
        
        // Afficher les agents
        function displayAgents() {
            const filteredAgents = agents.filter(agent => {
                if (currentCategory === 'all') return true;
                return agent.category === currentCategory;
            });
            
            if (currentView === 'grid') {
                displayAgentsGrid(filteredAgents);
            } else {
                displayAgentsList(filteredAgents);
            }
            
            document.getElementById('agentCount').textContent = filteredAgents.length;
        }
        
        // Afficher en grille
        function displayAgentsGrid(agents) {
            const container = document.getElementById('agentsGrid');
            container.innerHTML = '';
            
            agents.forEach(agent => {
                const card = document.createElement('div');
                card.className = `agent-card ${agent.category}`;
                card.innerHTML = `
                    <div class="agent-header">
                        <div class="agent-name">${agent.display_name}</div>
                        <div class="agent-status status-${agent.status}">
                            ${agent.status === 'active' ? '✅ Actif' : '⚠️ Inactif'}
                        </div>
                    </div>
                    <div class="agent-description">${agent.description}</div>
                    <div class="agent-meta">
                        <span>${agent.category}</span>
                        <span>${(agent.size / 1024).toFixed(1)} KB</span>
                    </div>
                `;
                
                card.onclick = () => executeAgent(agent.id, agent.name);
                container.appendChild(card);
            });
            
            document.getElementById('agentsGrid').style.display = 'grid';
            document.getElementById('agentsList').style.display = 'none';
        }
        
        // Afficher en liste
        function displayAgentsList(agents) {
            const container = document.getElementById('agentsList');
            container.innerHTML = '';
            
            const table = document.createElement('table');
            table.style.width = '100%';
            table.style.borderCollapse = 'collapse';
            
            agents.forEach(agent => {
                const row = table.insertRow();
                row.style.cursor = 'pointer';
                row.onclick = () => executeAgent(agent.id, agent.name);
                
                row.innerHTML = `
                    <td style="padding: 10px; border-bottom: 1px solid #eee;">
                        <strong>${agent.display_name}</strong><br>
                        <small style="color: #666;">${agent.description}</small>
                    </td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">
                        <span class="status-${agent.status}">${agent.status}</span>
                    </td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">
                        ${agent.category}
                    </td>
                    <td style="padding: 10px; border-bottom: 1px solid #eee; text-align: center;">
                        ${(agent.size / 1024).toFixed(1)} KB
                    </td>
                `;
            });
            
            container.appendChild(table);
            document.getElementById('agentsGrid').style.display = 'none';
            document.getElementById('agentsList').style.display = 'block';
        }
        
        // Afficher les catégories
        function displayCategories(categories) {
            const container = document.getElementById('categories');
            container.innerHTML = '';
            
            // Ajouter "Tous"
            const allItem = document.createElement('div');
            allItem.className = 'category-item';
            allItem.onclick = () => filterByCategory('all');
            allItem.innerHTML = `
                <i class="fas fa-layer-group"></i> Tous les agents
                <span class="category-count">${agents.length}</span>
            `;
            container.appendChild(allItem);
            
            // Ajouter chaque catégorie
            Object.entries(categories).forEach(([category, count]) => {
                const item = document.createElement('div');
                item.className = 'category-item';
                item.onclick = () => filterByCategory(category);
                item.innerHTML = `
                    <i class="fas fa-${getCategoryIcon(category)}"></i> ${category}
                    <span class="category-count">${count}</span>
                `;
                container.appendChild(item);
            });
        }
        
        // Afficher les infos système
        function displaySystemInfo(info) {
            const container = document.getElementById('systemInfo');
            container.innerHTML = `
                <div style="font-size: 12px; line-height: 1.6;">
                    <div><strong>OS:</strong> ${info.os}</div>
                    <div><strong>Python:</strong> ${info.python_version}</div>
                    <div><strong>Mémoire:</strong> ${info.memory_usage}%</div>
                    <div><strong>Uptime:</strong> ${info.uptime}</div>
                    <div><strong>Scan:</strong> ${info.last_scan}</div>
                </div>
            `;
        }
        
        // Exécuter un agent
        async function executeAgent(id, name) {
            addOutput(`> Lancement de ${name}...`);
            
            try {
                const response = await fetch(`/api/execute/${id}`);
                const result = await response.json();
                addOutput(`✅ ${result.message}`);
                
                // Mettre à jour le compteur d'agents actifs
                if (result.success) {
                    const activeEl = document.getElementById('activeAgents');
                    let active = parseInt(activeEl.textContent) || 0;
                    activeEl.textContent = active + 1;
                }
            } catch (error) {
                addOutput(`❌ Erreur: ${error.message}`);
            }
        }
        
        // Scanner les agents
        async function scanAgents() {
            addOutput('> Scan des agents en cours...');
            
            try {
                const response = await fetch('/api/agents?scan=true');
                agents = await response.json();
                displayAgents();
                loadCategories();
                addOutput(`✅ Scan terminé: ${agents.length} agents détectés`);
            } catch (error) {
                addOutput(`❌ Erreur de scan: ${error.message}`);
            }
        }
        
        // Filtrer par catégorie
        function filterByCategory(category) {
            currentCategory = category;
            displayAgents();
        }
        
        // Changer la vue
        function setView(view) {
            currentView = view;
            document.querySelectorAll('.view-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            displayAgents();
        }
        
        // Rechercher des agents
        function searchAgents() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            if (!searchTerm) return displayAgents();
            
            const filtered = agents.filter(agent => 
                agent.name.toLowerCase().includes(searchTerm) ||
                agent.display_name.toLowerCase().includes(searchTerm) ||
                agent.description.toLowerCase().includes(searchTerm)
            );
            
            if (currentView === 'grid') {
                displayAgentsGrid(filtered);
            } else {
                displayAgentsList(filtered);
            }
        }
        
        // Ajouter du texte à la sortie
        function addOutput(text) {
            const output = document.getElementById('outputContent');
            const timestamp = new Date().toLocaleTimeString('fr-FR');
            output.innerHTML += `\\n[${timestamp}] ${text}`;
            output.scrollTop = output.scrollHeight;
        }
        
        // Effacer la sortie
        function clearOutput() {
            document.getElementById('outputContent').innerHTML = '> Sortie effacée.';
        }
        
        // Afficher tous
        function showAll() {
            currentCategory = 'all';
            displayAgents();
        }
        
        // Afficher système
        function showSystem() {
            currentCategory = 'system';
            displayAgents();
        }
        
        // Obtenir l'icône d'une catégorie
        function getCategoryIcon(category) {
            const icons = {
                'web': 'globe',
                'ia': 'brain',
                'analyse': 'chart-bar',
                'system': 'server',
                'menu': 'bars',
                'general': 'file-code'
            };
            return icons[category] || 'file';
        }
        
        // Mettre à jour les statistiques
        function updateStats() {
            const active = agents.filter(a => a.status === 'active').length;
            document.getElementById('activeAgents').textContent = active;
        }
        
        // Rafraîchir automatiquement
        setInterval(() => {
            loadSystemInfo();
            updateStats();
        }, 30000);
        """
        self.wfile.write(js.encode('utf-8'))
    
    def send_json_agents(self):
        """Envoie la liste des agents en JSON"""
        # Rescan si demandé
        if 'scan=true' in self.path:
            self.scan_agents()
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(self.agents_cache, default=str).encode('utf-8'))
    
    def send_system_status(self):
        """Envoie le statut système"""
        import psutil
        
        status = {
            "os": "Alpine Linux",
            "python_version": sys.version.split()[0],
            "memory_usage": psutil.virtual_memory().percent,
            "cpu_usage": psutil.cpu_percent(),
            "uptime": time.strftime("%H:%M:%S", time.gmtime(time.time() - psutil.boot_time())),
            "last_scan": self.last_scan.isoformat() if self.last_scan else "Jamais",
            "agent_count": len(self.agents_cache)
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(status).encode('utf-8'))
    
    def send_categories(self):
        """Envoie les catégories disponibles"""
        categories = {}
        for agent in self.agents_cache:
            categories[agent["category"]] = categories.get(agent["category"], 0) + 1
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(categories).encode('utf-8'))
    
    def execute_agent(self, agent_id):
        """Exécute un agent"""
        try:
            agent_id = int(agent_id)
            if 0 <= agent_id < len(self.agents_cache):
                agent = self.agents_cache[agent_id]
                
                # Lancer l'agent dans un thread séparé
                thread = threading.Thread(target=self.run_agent, args=(agent,))
                thread.daemon = True
                thread.start()
                
                response = {
                    "success": True,
                    "message": f"Agent '{agent['name']}' lancé en arrière-plan",
                    "agent": agent["name"]
                }
            else:
                response = {"success": False, "message": "ID d'agent invalide"}
        except ValueError:
            response = {"success": False, "message": "ID d'agent invalide"}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def execute_agent_by_name(self, agent_name):
        """Exécute un agent par son nom"""
        for agent in self.agents_cache:
            if agent["name"] == agent_name:
                thread = threading.Thread(target=self.run_agent, args=(agent,))
                thread.daemon = True
                thread.start()
                return {"success": True, "message": f"Agent '{agent_name}' lancé"}
        
        return {"success": False, "message": f"Agent '{agent_name}' non trouvé"}
    
    def run_agent(self, agent):
        """Exécute réellement l'agent"""
        try:
            # Pour les interfaces web, on lance en arrière-plan
            if agent["category"] == "web":
                subprocess.Popen([sys.executable, agent["path"]], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
            else:
                # Pour les autres, on exécute normalement
                result = subprocess.run([sys.executable, agent["path"]], 
                                      capture_output=True, 
                                      text=True, 
                                      timeout=30)
                print(f"Agent {agent['name']} terminé: {result.returncode}")
        except Exception as e:
            print(f"Erreur exécution {agent['name']}: {e}")

def main():
    """Point d'entrée principal"""
    # Initialiser le scan
    AgentWebHandler.scan_agents()
    
    print("🌐 INTERFACE WEB UNIFIÉE POUR AGENTS IA")
    print("=" * 50)
    print(f"Port: {PORT}")
    print(f"Agents détectés: {len(AgentWebHandler.agents_cache)}")
    print(f"OS: Alpine Linux")
    print("\n📡 Informations:")
    print(f"  • Interface: http://localhost:{PORT}")
    print(f"  • Détection automatique: Activée")
    print(f"  • Catégories: {len(set(a['category'] for a in AgentWebHandler.agents_cache))}")
    print(f"  • Agents exécutables: {sum(1 for a in AgentWebHandler.agents_cache if a['status'] == 'active')}")
    print("\n🚀 Démarrage du serveur...")
    print("🛑 Arrêt: Ctrl+C")
    
    # Configurer le serveur
    handler = AgentWebHandler
    
    try:
        with socketserver.TCPServer(("", PORT), handler) as httpd:
            # Ouvrir dans le navigateur si possible
            try:
                webbrowser.open(f"http://localhost:{PORT}")
                print(f"✅ Navigateur ouvert automatiquement")
            except:
                print(f"📱 Ouvrez manuellement: http://localhost:{PORT}")
            
            print(f"✅ Serveur démarré avec succès!")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Vérifier les dépendances
    try:
        import psutil
    except ImportError:
        print("📦 Installation de psutil...")
        os.system(f"{sys.executable} -m pip install psutil --quiet")
    
    main()
EOF

# Rendre exécutable
chmod +x /root/interface_agents_web.py
