#!/usr/bin/env python3
"""
Test système complet de l'agent IA
"""

import sys
import os
import time
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_system_integration():
    """Test d'intégration du système"""
    print("🧪 TEST SYSTÈME COMPLET")
    print("=" * 60)
    
    # 1. Vérifier la structure des dossiers
    print("\n1. Vérification de la structure...")
    required_dirs = [
        'config',
        'src',
        'src/core',
        'src/modules',
        'src/bots',
        'storage',
        'storage/logs',
        'storage/memory'
    ]
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ (MANQUANT!)")
    
    # 2. Vérifier les fichiers essentiels
    print("\n2. Vérification des fichiers...")
    required_files = [
        'src/main.py',
        'src/core/agent.py',
        'config/settings.py',
        '.env',
        'requirements.txt',
        'README.md'
    ]
    
    for file_path in required_files:
        if Path(file_path).exists():
            size = Path(file_path).stat().st_size
            print(f"   ✅ {file_path} ({size} octets)")
        else:
            print(f"   ❌ {file_path} (MANQUANT!)")
    
    # 3. Test d'import des modules
    print("\n3. Test d'import des modules...")
    try:
        from src.core.agent import PersonalAIAgent
        print("   ✅ Module agent importé")
    except Exception as e:
        print(f"   ❌ Erreur import agent: {e}")
    
    try:
        from config.settings import config
        print("   ✅ Module config importé")
    except Exception as e:
        print(f"   ❌ Erreur import config: {e}")
    
    # 4. Test de création d'agent
    print("\n4. Test de création d'agent...")
    try:
        agent = PersonalAIAgent("Test Système")
        print(f"   ✅ Agent créé: {agent.name}")
        
        # Test rapide
        result = agent.process_input("Test système en cours")
        print(f"   ✅ Test de traitement: {result['analysis']['intent']}")
        
    except Exception as e:
        print(f"   ❌ Erreur création agent: {e}")
    
    # 5. Vérifier les logs
    print("\n5. Vérification des logs...")
    log_file = Path('storage/logs/agent.log')
    if log_file.exists():
        print(f"   ✅ Fichier de log existant: {log_file}")
    else:
        print(f"   ⚠️  Fichier de log non créé (sera créé au premier lancement)")
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DU TEST")
    print("=" * 60)
    print("Si toutes les vérifications sont OK, vous pouvez lancer:")
    print("  → python src/main.py      (pour l'agent complet)")
    print("  → python test_agent.py    (pour tester l'agent seul)")
    print("  → python test_interactive.py (pour mode conversation)")

if __name__ == "__main__":
    test_system_integration()
