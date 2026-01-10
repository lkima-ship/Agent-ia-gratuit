cat > src/modules/email_processor.py << 'EOF'
class EmailProcessor:
    def __init__(self):
        self.status = "prêt"
    
    def check_emails(self):
        return f"Module email: {self.status}"
EOF
