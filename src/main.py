cat > src/main.py << 'EOF'
#!/usr/bin/env python3
"""
Agent IA Gratuit - Version française
Assistant personnel pour emails, calendrier et notes vocales
"""

import os
import sys
import time

print("🤖 AGENT IA GRATUIT - FRANÇAIS")
print("=" * 50)

# Ajouter le chemin
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config.settings import config
    from src.core.agent import PersonalAIAgent
    from src.modules.email_processor import EmailProcessor
    
    print("✅ Configuration chargée")
    print(f"   📧 Email: {config.EMAIL_ADDRESS[:3]}***" if config.EMAIL_ADDRESS else "   📧 Email: Non configuré")
    print(f"   🗄️  Répertoire: {config.BASE_DIR}")
    
    # Initialiser l'agent
    agent = PersonalAIAgent("Assistant Personnel")
    print(f"\n🤖 {agent.greet()}")
    
    # Initialiser le module email
    email_module = EmailProcessor()
    print(f"📧 {email_module.check_emails()}")
    
    # Tester Outlook si configuré
    if hasattr(config, 'EMAIL_ADDRESS') and config.EMAIL_ADDRESS:
        print("\n🔍 Test de configuration Outlook...")
        
        try:
            from src.modules.outlook_client import OutlookClient
            
            masked_email = config.EMAIL_ADDRESS[:3] + "***"
            print(f"   Compte: {masked_email}")
            
            print("   Test automatique en cours...")
            
            client = OutlookClient(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
            
            if client.connect():
                count = client.get_unread_count()
                print(f"   ✅ Connecté - Emails non lus: {count}")
                client.disconnect()
            else:
                print("   ❌ Échec de connexion")
                print("   Vérifiez vos identifiants dans .env")
                
        except ImportError:
            print("   ℹ️  Module Outlook non disponible")
        except Exception as e:
            print(f"   ⚠️  Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 FONCTIONNALITÉS DISPONIBLES :")
    print("   1. 📧 Surveillance emails (Outlook)")
    print("   2. 🤖 Analyse IA basique")
    print("   3. 📁 Gestion de la structure")
    print("   4. 🔒 Protection des secrets")
    
    print("\n📝 PROCHAINES ÉTAPES :")
    print("   1. Développer le module calendrier")
    print("   2. Ajouter la transcription vocale")
    print("   3. Créer une interface web")
    print("   4. Automatiser les réponses")
    
    print("\n" + "=" * 50)
    print("💡 ASTUCE :")
    print("Vos secrets sont protégés dans .gitignore")
    print("NE partagez jamais votre fichier .env !")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
    print("Vérifiez que tous les modules sont installés")
except Exception as e:
    print(f"❌ Erreur générale: {e}")
EOF
