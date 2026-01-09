#!/usr/bin/env python3
"""
Agent IA Gratuit - Point d'entrée principal
Un assistant intelligent pour gérer emails, rendez-vous et notes vocales
"""

import asyncio
import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au chemin Python
sys.path.append(str(Path(__file__).parent.parent))

from src.core.agent import PersonalAIAgent
from src.modules.email_processor import EmailProcessor
from src.modules.ai_processor import AIProcessor
from config.settings import config
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('storage/logs/agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """Orchestrateur principal de l'agent IA"""
    
    def __init__(self):
        self.agent = None
        self.email_processor = None
        self.ai_processor = None
        self.is_running = False
        self.tasks = []
        
        logger.info("=" * 60)
        logger.info("🤖 AGENT IA GRATUIT - INITIALISATION")
        logger.info("=" * 60)
    
    def initialize(self):
        """Initialisation des composants"""
        try:
            # 1. Initialiser l'agent central
            self.agent = PersonalAIAgent(name="Assistant IA")
            logger.info("✅ Agent IA initialisé")
            
            # 2. Initialiser le processeur AI
            self.ai_processor = AIProcessor()
            logger.info("✅ Processeur AI initialisé")
            
            # 3. Initialiser le processeur email (si configuré)
            if config.EMAIL_ADDRESS and config.EMAIL_PASSWORD:
                self.email_processor = EmailProcessor()
                logger.info("✅ Module email prêt pour initialisation")
            else:
                logger.warning("⚠️  Email non configuré dans .env")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erreur d'initialisation: {e}")
            return False
    
    async def email_monitoring_task(self, interval=300):
        """Tâche de surveillance des emails"""
        if not self.email_processor:
            logger.warning("Module email non disponible")
            return
        
        try:
            # Se connecter aux emails
            if self.email_processor.connect():
                logger.info("📧 Connecté au serveur email")
            else:
                logger.error("❌ Échec de connexion email")
                return
        except Exception as e:
            logger.error(f"Erreur connexion email: {e}")
            return
        
        logger.info(f"👁️ Surveillance emails activée (intervalle: {interval}s)")
        
        while self.is_running:
            try:
                # Récupérer les nouveaux emails
                emails = self.email_processor.fetch_unread_emails(limit=5)
                
                if emails:
                    logger.info(f"📬 {len(emails)} nouveau(x) email(s) trouvé(s)")
                    
                    for email in emails:
                        await self.process_email(email)
                
                # Attendre avant la prochaine vérification
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Erreur surveillance emails: {e}")
                await asyncio.sleep(60)  # Attendre 1 minute en cas d'erreur
    
    async def process_email(self, email_data):
        """Traiter un email reçu"""
        try:
            logger.info(f"📨 Traitement email: {email_data['subject']}")
            
            # Analyser le contenu avec AI
            analysis = await self.ai_processor.analyze_email(
                email_data['subject'],
                email_data['body']
            )
            
            logger.info(f"📊 Analyse: Priorité: {analysis.get('priority')}, "
                       f"Catégorie: {analysis.get('category')}")
            
            # Décider de l'action
            action = await self.determine_email_action(email_data, analysis)
            
            # Exécuter l'action
            if action:
                await self.execute_action(action, email_data)
            
            # Marquer comme lu
            self.email_processor.mark_as_read(email_data['id'])
            
        except Exception as e:
            logger.error(f"Erreur traitement email: {e}")
    
    async def determine_email_action(self, email_data, analysis):
        """Déterminer l'action à prendre pour un email"""
        priority = analysis.get('priority', 'low')
        category = analysis.get('category', 'other')
        
        actions = []
        
        if priority == 'high':
            actions.append('notify')
        
        if category == 'meeting_request':
            actions.append('schedule_meeting')
        elif category == 'question':
            actions.append('generate_response')
        
        return {
            'email_id': email_data['id'],
            'sender': email_data['from'],
            'subject': email_data['subject'],
            'actions': actions,
            'analysis': analysis
        }
    
    async def execute_action(self, action, email_data):
        """Exécuter une action sur un email"""
        for action_type in action['actions']:
            if action_type == 'notify':
                self.notify_user(email_data)
            elif action_type == 'schedule_meeting':
                await self.schedule_meeting_from_email(email_data)
            elif action_type == 'generate_response':
                await self.generate_email_response(email_data)
    
    def notify_user(self, email_data):
        """Notifier l'utilisateur d'un email important"""
        logger.info(f"🔔 Notification: Email important de {email_data['from']}: "
                   f"{email_data['subject']}")
        # Ici, on pourrait envoyer une notification push, SMS, etc.
    
    async def schedule_meeting_from_email(self, email_data):
        """Programmer un rendez-vous depuis un email"""
        logger.info(f"📅 Tentative d'extraction de rendez-vous depuis email")
        # À implémenter avec le module calendrier
    
    async def generate_email_response(self, email_data):
        """Générer une réponse automatique"""
        logger.info(f"📝 Génération de réponse pour email")
        # À implémenter avec AI
    
    async def voice_processing_task(self):
        """Tâche de traitement des notes vocales"""
        logger.info("🎤 Module voix prêt")
        # À implémenter
    
    async def calendar_monitoring_task(self):
        """Tâche de surveillance du calendrier"""
        logger.info("📅 Module calendrier prêt")
        # À implémenter
    
    async def run(self):
        """Exécution principale de l'agent"""
        # Initialiser les composants
        if not self.initialize():
            logger.error("Échec de l'initialisation. Arrêt.")
            return
        
        self.is_running = True
        logger.info("🚀 Agent IA démarré avec succès!")
        
        try:
            # Démarrer les tâches en parallèle
            tasks = []
            
            # Tâche email si configuré
            if self.email_processor:
                tasks.append(self.email_monitoring_task(interval=60))
            
            # Tâche voix (placeholder)
            tasks.append(self.voice_processing_task())
            
            # Tâche calendrier (placeholder)
            tasks.append(self.calendar_monitoring_task())
            
            # Tâche de battement de cœur (health check)
            tasks.append(self.heartbeat_task())
            
            # Exécuter toutes les tâches
            await asyncio.gather(*tasks)
            
        except KeyboardInterrupt:
            logger.info("🛑 Arrêt demandé par l'utilisateur")
        except Exception as e:
            logger.error(f"Erreur critique: {e}")
        finally:
            await self.shutdown()
    
    async def heartbeat_task(self):
        """Tâche de santé pour montrer que l'agent est vivant"""
        counter = 0
        while self.is_running:
            counter += 1
            if counter % 10 == 0:  # Toutes les 10 itérations
                logger.info("❤️  Agent IA en cours d'exécution...")
            await asyncio.sleep(10)
    
    async def shutdown(self):
        """Arrêt propre de l'agent"""
        logger.info("🧹 Nettoyage avant arrêt...")
        self.is_running = False
        
        # Fermer les connexions
        if self.email_processor:
            self.email_processor.disconnect()
        
        logger.info("👋 Agent arrêté proprement")

def main():
    """Point d'entrée principal"""
    # Créer les dossiers nécessaires
    os.makedirs('storage/logs', exist_ok=True)
    
    try:
        # Créer et exécuter l'orchestrateur
        orchestrator = AgentOrchestrator()
        asyncio.run(orchestrator.run())
        
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
