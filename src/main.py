#!/usr/bin/env python3
"""
Agent IA Professionnel - Point d'entrée principal
Version basique - Étape 1
"""

import asyncio
import time
from loguru import logger
import sys

# Ajouter le dossier src au path
sys.path.append('src')

from core.agent import PersonalAIAgent
from modules.email_processor import EmailProcessor
from config.settings import settings

class AgentOrchestrator:
    """Orchestrateur de l'agent IA"""
    
    def __init__(self):
        self.agent = PersonalAIAgent(name="Assistant Personnel")
        self.email_processor = EmailProcessor(
            imap_server=settings.EMAIL_IMAP_SERVER,
            port=settings.EMAIL_IMAP_PORT
        )
        self.running = False
        
        logger.info("=" * 50)
        logger.info(" 🚀 INITIALISATION AGENT IA PROFESSIONNEL")
        logger.info("=" * 50)
    
    def check_configuration(self) -> bool:
        """Vérification de la configuration"""
        logger.info("🔧 Vérification de la configuration...")
        
        # Vérifier les variables d'environnement
        required_vars = ['EMAIL_ADDRESS', 'EMAIL_PASSWORD']
        missing = []
        
        for var in required_vars:
            if not getattr(settings, var, None):
                missing.append(var)
        
        if missing:
            logger.error(f"❌ Variables manquantes: {', '.join(missing)}")
            logger.info("Copiez .env.example en .env et remplissez les valeurs")
            return False
        
        logger.success("✅ Configuration validée")
        return True
    
    async def initialize_email(self) -> bool:
        """Initialisation du module email"""
        logger.info("📧 Initialisation du module email...")
        
        if self.email_processor.connect(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD):
            logger.success("✅ Module email initialisé")
            return True
        else:
            logger.error("❌ Échec initialisation email")
            return False
    
    async def email_monitoring_loop(self, interval: int = 300):
        """Boucle de surveillance des emails"""
        logger.info(f"👁️ Surveillance emails activée (intervalle: {interval}s)")
        
        while self.running:
            try:
                # Récupérer les nouveaux emails
                emails = self.email_processor.fetch_unread_emails(limit=5)
                
                if emails:
                    logger.info(f"📬 {len(emails)} nouveau(x) email(s) trouvé(s)")
                    
                    for email in emails:
                        # Analyser avec l'agent
                        analysis = self.agent.analyze_text(email['body'])
                        intent = self.agent.classify_intent(email['body'])
                        
                        logger.info(f"""
                        📨 Nouvel email:
                        De: {email['from']}
                        Sujet: {email['subject']}
                        Intention détectée: {intent}
                        Résumé: {analysis['summary']}
                        """)
                        
                        # Marquer comme lu (optionnel)
                        # self.email_processor.mark_as_read(email['id'])
                
                # Attendre avant la prochaine vérification
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erreur surveillance emails: {e}")
                await asyncio.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    async def run(self):
        """Exécution principale de l'agent"""
        logger.info("🚀 Démarrage de l'agent...")
        
        # Vérifier la configuration
        if not self.check_configuration():
            return
        
        # Initialiser les modules
        email_ok = await self.initialize_email()
        
        if not email_ok:
            logger.warning("⚠️  Agent démarré sans module email")
        
        # Démarrer la boucle principale
        self.running = True
        logger.success("🎉 Agent IA démarré avec succès!")
        
        try:
            # Lancer la surveillance emails
            if email_ok:
                await self.email_monitoring_loop(interval=60)  # Vérifier toutes les minutes
            
            # Boucle principale simple pour l'instant
            while self.running:
                # Ici on ajoutera d'autres tâches plus tard
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt demandé par l'utilisateur")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Nettoyage à l'arrêt"""
        logger.info("🧹 Nettoyage avant arrêt...")
        self.running = False
        self.email_processor.disconnect()
        logger.info("👋 Agent arrêté")

async def main():
    """Point d'entrée principal"""
    orchestrator = AgentOrchestrator()
    await orchestrator.run()

if __name__ == "__main__":
    # Démarrer l'agent
    asyncio.run(main())
