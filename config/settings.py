import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Settings:
    # Chemins
    BASE_DIR = Path(__file__).parent.parent
    
    # Configuration Email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_IMAP_SERVER = os.getenv("EMAIL_IMAP_SERVER", "imap.gmail.com")
    EMAIL_IMAP_PORT = int(os.getenv("EMAIL_IMAP_PORT", 993))
    
    # Configuration AI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")
    
    # Configuration Calendrier
    CALENDAR_PROVIDER = os.getenv("CALENDAR_PROVIDER", "google")
    
    # Chemins de stockage
    STORAGE_DIR = BASE_DIR / "storage"
    LOGS_DIR = STORAGE_DIR / "logs"
    
    def __init__(self):
        # Créer les dossiers nécessaires
        self.STORAGE_DIR.mkdir(exist_ok=True)
        self.LOGS_DIR.mkdir(exist_ok=True)

# Instance globale
settings = Settings()
