cat > /root/plugin_manager.py << 'EOF'
#!/usr/bin/env python3
"""
GESTIONNAIRE DE PLUGINS DYNAMIQUES
"""
import os
import sys
import importlib.util
import json
from pathlib import Path

class PluginManager:
    """Gestion dynamique des plugins"""
    
    def __init__(self, plugins_dir="/root/plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        self.plugins = {}
        self._charger_plugins()
    
    def _charger_plugins(self):
        """Charge tous les plugins disponibles"""
        for plugin_file in self.plugins_dir.glob("*.py"):
            plugin_name = plugin_file.stem
            try:
                spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                self.plugins[plugin_name] = {
                    "module": module,
                    "file": plugin_file,
                    "metadata": getattr(module, "PLUGIN_METADATA", {})
                }
                print(f"✅ Plugin chargé : {plugin_name}")
            except Exception as e:
                print(f"❌ Erreur chargement {plugin_name}: {e}")
    
    def executer_plugin(self, plugin_name, *args, **kwargs):
        """Exécute un plugin spécifique"""
        if plugin_name in self.plugins:
            plugin = self.plugins[plugin_name]
            if hasattr(plugin["module"], "execute"):
                return plugin["module"].execute(*args, **kwargs)
        return {"erreur": f"Plugin {plugin_name} non trouvé"}
    
    def creer_plugin(self, nom, code):
        """Crée un nouveau plugin dynamiquement"""
        plugin_path = self.plugins_dir / f"{nom}.py"
        plugin_path.write_text(code)
        print(f"📦 Plugin créé : {plugin_path}")
        self._charger_plugins()
        return str(plugin_path)

# Plugins par défaut
plugins_par_defaut = {
    "web_scraper": """
PLUGIN_METADATA = {
    "name": "Web Scraper",
    "version": "1.0",
    "description": "Scraping web intelligent"
}

def execute(url=None):
    import requests
    from bs4 import BeautifulSoup
    
    if not url:
        return {"erreur": "URL requise"}
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            "url": url,
            "status": response.status_code,
            "title": soup.title.string if soup.title else "N/A",
            "links": len(soup.find_all('a'))
        }
    except Exception as e:
        return {"erreur": str(e)}
""",
    
    "data_analyzer": """
PLUGIN_METADATA = {
    "name": "Data Analyzer",
    "version": "1.0",
    "description": "Analyse de données basique"
}

def execute(data=None):
    if not data:
        return {"erreur": "Données requises"}
    
    try:
        # Analyse simple
        if isinstance(data, list):
            stats = {
                "count": len(data),
                "min": min(data) if data else None,
                "max": max(data) if data else None,
                "avg": sum(data)/len(data) if data else None
            }
            return stats
        else:
            return {"type": type(data).__name__, "length": len(str(data))}
    except Exception as e:
        return {"erreur": str(e)}
""",
    
    "system_monitor": """
PLUGIN_METADATA = {
    "name": "System Monitor",
    "version": "1.0",
    "description": "Surveillance système"
}

def execute():
    import os
    import psutil
    
    stats = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent,
        "processes": len(psutil.pids())
    }
    return stats
"""
}

def initialiser_plugins():
    """Initialise les plugins par défaut"""
    manager = PluginManager()
    
    # Créer les plugins par défaut s'ils n'existent pas
    for nom, code in plugins_par_defaut.items():
        plugin_path = manager.plugins_dir / f"{nom}.py"
        if not plugin_path.exists():
            plugin_path.write_text(code)
            print(f"📦 Plugin créé : {nom}")
    
    manager._charger_plugins()
    return manager

def interface_plugins():
    """Interface de gestion des plugins"""
    manager = initialiser_plugins()
    
    print("""
    🧩 GESTIONNAIRE DE PLUGINS DYNAMIQUES
    ======================================
    """)
    
    while True:
        print(f"\n📦 Plugins disponibles ({len(manager.plugins)}) :")
        for i, (nom, plugin) in enumerate(manager.plugins.items(), 1):
            meta = plugin["metadata"]
            print(f"{i}. {nom} - {meta.get('description', 'Sans description')}")
        
        print("\n🔧 Actions :")
        print("1. Exécuter un plugin")
        print("2. Créer un nouveau plugin")
        print("3. Lister tous les plugins")
        print("4. Rafraîchir les plugins")
        print("0. Retour")
        
        choix = input("\n👉 Votre choix : ")
        
        if choix == "1":
            if manager.plugins:
                print("\n🎯 Plugins disponibles :")
                for nom in manager.plugins.keys():
                    print(f"  • {nom}")
                
                plugin_nom = input("\nNom du plugin à exécuter : ")
                if plugin_nom in manager.plugins:
                    # Demander les paramètres
                    params = input("Paramètres (séparés par virgule) : ")
                    args = params.split(',') if params else []
                    
                    resultat = manager.executer_plugin(plugin_nom, *args)
                    print(f"\n📊 Résultat : {resultat}")
                else:
                    print("❌ Plugin non trouvé")
            else:
                print("❌ Aucun plugin disponible")
        
        elif choix == "2":
            print("\n🛠️ Création d'un nouveau plugin")
            nom = input("Nom du plugin : ")
            print("\n📝 Éditeur de code (tapez 'END' sur une ligne vide pour terminer) :")
            
            lignes = []
            while True:
                ligne = input()
                if ligne.strip() == "END":
                    break
                lignes.append(ligne)
            
            code = "\n".join(lignes)
            manager.creer_plugin(nom, code)
            print(f"✅ Plugin {nom} créé avec succès !")
        
        elif choix == "3":
            print("\n📋 LISTE COMPLÈTE DES PLUGINS :")
            for nom, plugin in manager.plugins.items():
                meta = plugin["metadata"]
                print(f"\n🔹 {nom}")
                print(f"   Description: {meta.get('description', 'N/A')}")
                print(f"   Version: {meta.get('version', 'N/A')}")
                print(f"   Fichier: {plugin['file']}")
        
        elif choix == "4":
            manager._charger_plugins()
            print(f"✅ Plugins rafraîchis : {len(manager.plugins)} chargés")
        
        elif choix == "0":
            break
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    interface_plugins()
EOF
