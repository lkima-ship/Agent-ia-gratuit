cat > src/core/agent.py << 'EOF'
import json
from datetime import datetime
from typing import Dict, Any

class PersonalAIAgent:
    """Agent IA personnel avec mémoire de base"""
    
    def __init__(self, name: str = "Assistant IA"):
        self.name = name
        self.context = {}
        print(f"🤖 {self.name} initialisé")
    
    def greet(self) -> str:
        """Message de salutation"""
        return f"Bonjour, je suis {self.name} ! Prêt à vous aider."
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyse basique d'un texte"""
        return {
            "length": len(text),
            "words": len(text.split()),
            "language": "fr",  # À améliorer
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne l'état de l'agent"""
        return {
            "name": self.name,
            "status": "running",
            "context_keys": list(self.context.keys())
        }

if __name__ == "__main__":
    # Test de l'agent
    agent = PersonalAIAgent("Test Agent")
    print(agent.greet())
    print(agent.analyze_text("Bonjour, comment ça va ?"))
EOF
