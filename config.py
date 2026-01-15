# config.py - Configuration centralisée
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentConfig:
    # Modèles IA
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    huggingface_token: Optional[str] = os.getenv("HF_TOKEN")
    
    # Base de données
    db_url: str = os.getenv("DB_URL", "sqlite:///agent.db")
    
    # Paramètres de performance
    max_workers: int = 4
    cache_ttl: int = 3600
    
    # Personnalisation
    agent_personality: str = "helpful"  # helpful, professional, casual
    language: str = "fr"
    
    @classmethod
    def from_env(cls):
        return cls()
