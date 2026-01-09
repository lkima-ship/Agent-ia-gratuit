#!/usr/bin/env python3
"""
Test simple de l'agent IA
"""

import sys
import os

# Ajouter le dossier src au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.agent import PersonalAIAgent

def test_agent_basics():
    """Test des fonctionnalités de base de l'agent"""
    print("🧪 TEST DE L'AGENT IA")
    print("=" * 50)
    
    # 1. Création de l'agent
    print("\n1. Création de l'agent...")
    agent = PersonalAIAgent(name="Assistant Test")
    print(f"✅ Agent créé: {agent.name}")
    
    # 2. Test de traitement d'entrée
    print("\n2. Test de traitement d'entrée...")
    test_inputs = [
        "Bonjour, peux-tu vérifier mes emails ?",
        "Je dois prendre un rendez-vous avec Jean demain",
        "Transcris ma note vocale s'il te plaît",
        "C'est urgent !"
    ]
    
    for i, input_text in enumerate(test_inputs, 1):
        print(f"\n   Test {i}: '{input_text}'")
        result = agent.process_input(input_text)
        print(f"   → Réponse: {result['response']}")
        print(f"   → Intent détectée: {result['analysis']['intent']}")
        print(f"   → Urgence: {result['analysis']['urgency']}")
    
    # 3. Test des commandes
    print("\n3. Test des commandes...")
    commands = [
        ("get_stats", {}),
        ("set_preference", {"key": "langue", "value": "français"}),
    ]
    
    for cmd, params in commands:
        print(f"\n   Commande: {cmd}")
        result = agent.execute_command(cmd, params)
        print(f"   → Succès: {result['success']}")
        print(f"   → Résultat: {result['result']}")
    
    # 4. Vérification mémoire
    print("\n4. Vérification de la mémoire...")
    stats = agent.get_context_summary()
    print(f"   Conversations: {stats['memory_stats']['total_conversations']}")
    print(f"   Décisions: {stats['memory_stats']['total_decisions']}")
    print(f"   Préférences: {stats['user_preferences']}")
    
    print("\n" + "=" * 50)
    print("✅ TESTS TERMINÉS AVEC SUCCÈS !")
    print("=" * 50)

if __name__ == "__main__":
    test_agent_basics()
