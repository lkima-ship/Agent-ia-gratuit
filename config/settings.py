cat > config/settings.py << 'EOF'
import os

class Config:
    # Configuration Email
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS", "")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
    
    # Configuration AI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Chemins
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

config = Config()
EOF
