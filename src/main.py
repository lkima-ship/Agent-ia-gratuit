cat > src/main.py << 'EOF'
#!/usr/bin/env python3
print("🤖 AGENT IA GRATUIT")
print("=" * 30)

# Importer les modules
from src.core.agent import PersonalAIAgent
from src.modules.email_processor import EmailProcessor

# Initialiser l'agent
agent = PersonalAIAgent("Assistant Personnel")
print(f"1. {agent.greet()}")

# Initialiser le module email
email_module = EmailProcessor()
print(f"2. {email_module.check_emails()}")

print("\n✅ Tous les modules sont initialisés !")
print("📁 Structure complète créée avec succès.")
print("\nProchaines étapes :")
print("1. Configurer .env avec vos clés API")
print("2. Développer les fonctionnalités d'email")
print("3. Ajouter le module calendrier")
print("4. Ajouter le module notes vocales")
EOF
