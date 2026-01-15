# Dans plugin_system.py
class PluginSystem:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()
    
    def load_plugins(self):
        # Chargement dynamique de plugins
        plugins_dir = "plugins/"
        for file in os.listdir(plugins_dir):
            if file.endswith("_plugin.py"):
                plugin = import_plugin(file)
                self.plugins[plugin.name] = plugin
    
    def execute_plugin(self, plugin_name, *args):
        if plugin_name in self.plugins:
            return self.plugins[plugin_name].execute(*args)
