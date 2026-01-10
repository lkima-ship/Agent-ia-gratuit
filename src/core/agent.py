cat > src/core/agent.py << 'EOF'
class PersonalAIAgent:
    def __init__(self, name="Assistant IA"):
        self.name = name
    
    def greet(self):
        return f"Bonjour, je suis {self.name} !"
EOF
