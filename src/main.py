#!/usr/bin/env python3
"""
ASSISTANT IA 100% GRATUIT
Point d'entrée principal
"""

import os
import sys
from dotenv import load_dotenv

# Charger configuration
load_dotenv()

def main():
    print("""
    ╔══════════════════════════════════════════╗
    ║    🤖 ASSISTANT IA 100% GRATUIT         ║
    ║                                          ║
    ║  📧 Réponses emails automatiques        ║
    ║  📅 Gestion de rendez-vous              ║
    ║  📞 Traitement messages vocaux          ║
    ║  🎯 Entièrement gratuit & Open Source   ║
    ╚══════════════════════════════════════════╝
    """)
    
    print("🎯 Sélectionnez un mode :")
    print("1. 🚀 Mode Web Interface")
    print("2. 🤖 Mode Telegram Bot")
    print("3. ⚙️  Mode API")
    print("4. 📧 Mode Email Processor")
    print("5. ❌ Quitter")
    
    choix = input("\nVotre choix (1-5): ").strip()
    
    if choix == "1":
        from src.web_app import run_web_app
        run_web_app()
    elif choix == "2":
        from src.bots.telegram_bot import run_telegram_bot
        run_telegram_bot()
    elif choix == "3":
        from src.api_server import run_api
        run_api()
    elif choix == "4":
        from src.modules.email_handler import run_email_processor
        run_email_processor()
    else:
        print("👋 Au revoir !")
        sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Interruption")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        sys.exit(1)
