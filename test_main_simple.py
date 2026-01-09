#!/usr/bin/env python3
"""
Version simplifiée de main.py pour test
"""

import sys
import os
import asyncio
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.agent import PersonalAIAgent

class SimpleAgentRunner:
    """Version simplifiée de l'agent"""
    
    def __init__(self):
        self.agent = PersonalAIAgent("Assistant Simple")
        self.running = False
        
    async def run_demo(self, duration=30):
        """Exécute une démo de l'agent"""
        self.running = True
        
        print("🚀 DÉMO DE L'AGENT IA")
        print("=" * 50)
        print("L'agent va simuler le traitement de différentes tâches...")
        print(f"Durée: {duration} secondes")
        print("=" * 50)
        
        start_time = time.time()
        task_count = 0
        
        while self.running and (time.time() - start_time) < duration:
            try:
                # Simuler différentes tâches
                tasks = [
                    "Vérifier les nouveaux emails",
                    "Analyser une demande de rendez-vous",
                    "Traiter une note vocale",
                    "Générer un rapport quotidien"
                ]
                
                for task in tasks:
                    if not self.running or (time.time() - start_time) >= duration:
                        break
                    
                    print(f"\n📋 Tâche: {task}")
                    
                    # Simuler le traitement
                    await asyncio.sleep(1)
                    
                    # Traiter avec l'agent
                    result = self.agent.process_input(task)
                    
                    print(f"   🤖 Réponse: {result['response']}")
                    print(f"   🔍 Analyse: {result['analysis']}")
                    
                    task_count += 1
                    
                    # Attendre un peu
                    await asyncio.sleep(2)
                
            except KeyboardInterrupt:
                print("\n🛑 Démarré interrompue")
                break
            except Exception as e:
                print(f"❌ Erreur: {e}")
                await asyncio.sleep(1)
        
        # Afficher le résumé
        print("\n" + "=" * 50)
        print("📊 RÉSUMÉ DE LA DÉMO")
        print("=" * 50)
        print(f"Tâches traitées: {task_count}")
        print(f"Durée totale: {time.time() - start_time:.1f}s")
        
        stats = self.agent.get_context_summary()
        print(f"Conversations en mémoire: {stats['memory_stats']['total_conversations']}")
        
        self.running = False
        print("\n✅ Démarré terminée avec succès !")

async def main():
    """Point d'entrée"""
    runner = SimpleAgentRunner()
    await runner.run_demo(duration=20)  # 20 secondes de démo

if __name__ == "__main__":
    asyncio.run(main())
