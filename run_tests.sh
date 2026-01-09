#!/bin/bash

echo "🧪 LANCEMENT DES TESTS DE L'AGENT IA"
echo "======================================"

# 1. Test système
echo -e "\n1. Test système..."
python test_system.py

# 2. Test agent basique
echo -e "\n\n2. Test agent basique..."
python test_agent.py

# 3. Test version simplifiée
echo -e "\n\n3. Test version simplifiée..."
python test_main_simple.py

echo -e "\n\n✅ TOUS LES TESTS SONT TERMINÉS !"
echo -e "\nProchaines étapes:"
echo "  → python src/main.py        # Lancer l'agent complet"
echo "  → python test_interactive.py # Mode conversation"
