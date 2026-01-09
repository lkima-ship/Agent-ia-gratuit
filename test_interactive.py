#!/usr/bin/env python3
"""
Test interactif de l'agent IA
"""

import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.agent import PersonalAIAgent

class InteractiveTester:
    def __init__(self):
        self.agent = PersonalAIAgent(name="Assistant Interactif")
        self.running = False
        
    async def run(self):
        """Lance le mode interactif"""
        self.running = True
        
        print("🤖 AGENT IA - MODE INTERACTIF")
        print("=" * 50)
        print("Commandes spéciales:")
        print("  /stats   - Afficher les statistiques")
        print("  /clear   - Effacer la mémoire")
        print("  /prefs   - Afficher les préférences")
        print("  /quit    - Quitter")
        print("=" * 50)
        print("\nParlez à votre assistant IA...\n")
        
        while self.running:
            try:
                # Lire l'entrée utilisateur
                user_input = input("👤 Vous: ").strip()
                
                if not user_input:
                    continue
                
                # Commandes spéciales
                if user_input.startswith('/'):
                    await self.handle_command(user_input)
                    continue
                
                # Traitement normal
                result = self.agent.process_input(user_input)
                
                # Afficher la réponse
                print(f"🤖 {self.agent.name}: {result['response']}")
                
                # Afficher des détails si demandé
                if result['analysis']['urgency'] == 'high':
                    print(f"   ⚠️  Message marqué comme urgent")
                
            except KeyboardInterrupt:
                print("\n\n👋 Au revoir !")
                self.running = False
            except Exception as e:
                print(f"❌ Erreur: {e}")
    
    async def handle_command(self, command):
        """Gère les commandes spéciales"""
        cmd = command.lower().strip()
        
        if cmd == '/quit':
            print("👋 Fermeture de l'agent...")
            self.running = False
            
        elif cmd == '/stats':
            stats = self.agent.get_context_summary()
            print("\n📊 STATISTIQUES:")
            print(f"   Nom: {stats['agent_name']}")
            print(f"   Statut: {stats['system_status']}")
            print(f"   Conversations récentes: {stats['recent_interactions_count']}")
            print(f"   Mémoire totale: {stats['memory_stats']['total_conversations']}")
            
        elif cmd == '/clear':
            confirm = input("⚠️  Effacer toute la mémoire ? (oui/non): ")
            if confirm.lower() == 'oui':
                self.agent.execute_command('clear_memory', {})
                print("✅ Mémoire effacée")
            else:
                print("❌ Annulé")
                
        elif cmd == '/prefs':
            prefs = self.agent.memory.preferences
            if prefs:
                print("\n⚙️  PRÉFÉRENCES:")
                for key, value in prefs.items():
                    print(f"   {key}: {value}")
            else:
                print("📝 Aucune préférence définie")
                
        else:
            print("❌ Commande non reconnue. Tapez /help pour la liste.")

def main():
    """Point d'entrée"""
    tester = InteractiveTester()
    
    try:
        asyncio.run(tester.run())
    except KeyboardInterrupt:
        print("\n👋 Test interrompu")

if __name__ == "__main__":
    main()
