cat > /root/config_agents.py << 'EOF'
#!/usr/bin/env python3
"""
Configuration centralisée pour tous les agents
"""

# Chemins des agents
AGENTS = {
    1: {"nom": "Agent IA ML", "fichier": "/root/agent_ia_ml.py", "actif": True},
    2: {"nom": "Analyse Données", "fichier": "/root/agent_analyse_donnees.py", "actif": True},
    3: {"nom": "Agent Web Avancé", "fichier": "/root/agent_web_avance_v2.py", "actif": True},
    4: {"nom": "Surveillance Système", "fichier": "/root/agent_surveillance.py", "actif": True},
    5: {"nom": "Agent IA Pro", "fichier": "/root/agent_ia_pro.py", "actif": True},
    6: {"nom": "Agent IA Gratuit", "fichier": "/root/agent_ia_gratuit.py", "actif": True},
    7: {"nom": "Agent IA Complet", "fichier": "/root/agent_ia_complet.py", "actif": True},
    8: {"nom": "Hub Agents", "fichier": "/root/hub_agents.py", "actif": True},
    9: {"nom": "Agent Web Simple", "fichier": "/root/agent_web_avance.py", "actif": True},
    10: {"nom": "Menu Commandes", "fichier": "/root/menu_master_v2.py", "actif": True}
}

# Paramètres communs
PARAMS = {
    "log_dir": "/root/logs",
    "data_dir": "/root/data",
    "cache_dir": "/root/.cache",
    "langue": "fr",
    "debug": True,
    "timeout": 30
}

# URLs de référence
URLS = {
    "github": "https://github.com/Agent-ia-gratuit",
    "doc": "https://github.com/Agent-ia-gratuit/docs",
    "api_base": "https://api.agent-ia.com"
}
EOF
