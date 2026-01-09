import json
from loguru import logger
from typing import Dict, Any
import sys

# Configurer les logs
logger.remove()
logger.add(sys.stdout, format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>")
logger.add("storage/logs/agent.log", rotation="1 day")

class PersonalAIAgent:
    """Agent IA de base avec logging"""
    
    def __init__(self, name: str = "Assistant IA"):
        self.name = name
        self.context = {}
        logger.info(f"✅ Agent '{self.name}' initialisé")
    
    def log(self, message: str, level: str = "info"):
        """Journalisation simplifiée"""
        log_func = getattr(logger, level)
        log_func(f"[{self.name}] {message}")
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyse basique d'un texte"""
        self.log(f"Analyse du texte: {text[:100]}...")
        
        # Pour l'instant, analyse simple
        # On intégrera l'IA plus tard
        return {
            "length": len(text),
            "words": len(text.split()),
            "language": "fr",  # Détection basique
            "summary": text[:200] + "..." if len(text) > 200 else text
        }
    
    def classify_intent(self, text: str) -> str:
        """Classification basique de l'intention"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["rdv", "rendez-vous", "meeting", "réunion"]):
            return "schedule_meeting"
        elif any(word in text_lower for word in ["email", "mail", "courriel"]):
            return "send_email"
        elif any(word in text_lower for word in ["appelle", "téléphone", "phone"]):
            return "call"
        elif any(word in text_lower for word in ["rappelle", "rappel", "souviens"]):
            return "reminder"
        else:
            return "unknown"
    
    def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extraction d'entités basique"""
        # On améliorera avec NLP plus tard
        return {
            "dates": [],
            "times": [],
            "people": [],
            "locations": []
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Retourne l'état de l'agent"""
        return {
            "name": self.name,
            "context_size": len(self.context),
            "status": "running"
        }
