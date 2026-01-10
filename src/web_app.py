# Créer le fichier web_app.py minimal
cat > src/web_app.py << 'EOF'
"""
Application web FastAPI
"""

from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Agent IA Gratuit API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF
