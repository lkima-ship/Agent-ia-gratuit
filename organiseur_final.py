cat > organiseur_final.py << 'EOF'
#!/usr/bin/env python3
# ORGANISATEUR FINAL - Script simple d'organisation

import os
import shutil
import sys

print("🚀 DÉMARRAGE DE L'ORGANISATION")
print("="*50)

# 1. Créer les dossiers essentiels
print("\n📁 CRÉATION DES DOSSIERS...")
dossiers = ['AGENTS', 'APIS', 'SCRIPTS', 'WEB', 'PROJETS', 'DATA', 'TESTS', 'MENUS']
for d in dossiers:
    if not os.path.exists(d):
        os.makedirs(d)
        print(f"✅ {d}")

# 2. Organiser les fichiers actuels
print("\n🔄 ORGANISATION DES FICHIERS...")
fichiers = [f for f in os.listdir('.') if os.path.isfile(f) and f != 'organiseur_final.py']

for f in fichiers:
    nom = f.lower()
    
    if 'agent' in nom:
        dest = 'AGENTS'
    elif 'api' in nom or 'flask' in nom or 'server' in nom:
        dest = 'APIS'
    elif 'menu' in nom:
        dest = 'MENUS'
    elif nom.endswith('.sh'):
        dest = 'SCRIPTS'
    elif nom.endswith(('.html', '.htm')):
        dest = 'WEB'
    elif nom.endswith('.py'):
        if 'agent' in nom:
            dest = 'AGENTS'
        elif 'api' in nom or 'web' in nom:
            dest = 'APIS'
        elif 'test' in nom:
            dest = 'TESTS'
        else:
            dest = 'SCRIPTS'
    elif nom.endswith(('.log', '.db', '.txt', '.json', '.yaml')):
        dest = 'DATA'
    else:
        dest = 'PROJETS'
    
    try:
        shutil.move(f, os.path.join(dest, f))
        print(f"📦 {f} → {dest}/")
    except:
        print(f"⚠  {f} (déjà déplacé)")

# 3. Créer le menu principal SIMPLE
print("\n📝 CRÉATION DU MENU...")
menu_code = '''#!/usr/bin/env python3
# menu_principal.py - Menu simple

import os
import subprocess

print("🤖 MENU PRINCIPAL - VOS PROJETS")
print("="*40)

while True:
    print()
    print("1. 📊 Voir les statistiques")
    print("2. 🤖 Voir les agents IA")
    print("3. 🌐 Voir les APIs")
    print("4. 🛠️  Voir les scripts")
    print("5. 🚀 Démarrer un agent")
    print("6. 🔄 Réorganiser les fichiers")
    print("7. ❌ Quitter")
    
    choix = input("👉 Votre choix: ")
    
    if choix == "1":
        print()
        print("📊 STATISTIQUES:")
        for d in ['AGENTS', 'APIS', 'SCRIPTS', 'WEB', 'PROJETS']:
            if os.path.exists(d):
                nb = len([f for f in os.listdir(d) if os.path.isfile(os.path.join(d, f))])
                print(f"  {d}: {nb} fichiers")
    
    elif choix == "2":
        print()
        print("🤖 AGENTS IA:")
        if os.path.exists('AGENTS'):
            for f in os.listdir('AGENTS'):
                if f.endswith('.py'):
                    print(f"  📄 {f}")
    
    elif choix == "3":
        print()
        print("🌐 APIS:")
        if os.path.exists('APIS'):
            for f in os.listdir('APIS'):
                print(f"  📄 {f}")
    
    elif choix == "4":
        print()
        print("🛠️  SCRIPTS:")
        if os.path.exists('SCRIPTS'):
            for f in os.listdir('SCRIPTS'):
                print(f"  📄 {f}")
    
    elif choix == "5":
        if os.path.exists('AGENTS'):
            agents = [f for f in os.listdir('AGENTS') if f.endswith('.py')]
            if agents:
                print()
                print("Choisissez un agent:")
                for i, agent in enumerate(agents, 1):
                    print(f"  {i}. {agent}")
                
                try:
                    choix_agent = int(input("👉 Numéro: ")) - 1
                    if 0 <= choix_agent < len(agents):
                        print(f"\n🚀 Lancement: {agents[choix_agent]}")
                        subprocess.run(['python3', f'AGENTS/{agents[choix_agent]}'])
                except:
                    print("❌ Choix invalide")
    
    elif choix == "6":
        print("\n🔄 Réorganisation...")
        subprocess.run(['python3', 'organiseur_final.py'])
    
    elif choix == "7":
        print("\n👋 Au revoir!")
        break
    
    else:
        print("\n❌ Choix invalide!")
    
    input("\n↵ Appuyez sur Entrée pour continuer...")
'''

with open('menu_principal.py', 'w') as f:
    f.write(menu_code)

# 4. Créer un script de démarrage
start_code = '''#!/bin/bash
# start_system.sh - Démarrage simple

echo "=========================================="
echo "🚀 SYSTÈME IA - PRÊT À UTILISER"
echo "=========================================="
echo ""
echo "📁 Structure créée:"
for d in AGENTS APIS SCRIPTS WEB PROJETS; do
    if [ -d "$d" ]; then
        count=$(ls "$d" | wc -l)
        echo "  $d: $count fichiers"
    fi
done
echo ""
echo "🚀 Commandes disponibles:"
echo "  python3 menu_principal.py    # Menu principal"
echo "  ls AGENTS/                   # Voir les agents"
echo "  ls APIS/                     # Voir les APIs"
echo "  python3 organiseur_final.py  # Réorganiser"
echo ""
echo "=========================================="
'''

with open('start_system.sh', 'w') as f:
    f.write(start_code)

# Rendre exécutables
os.chmod('menu_principal.py', 0o755)
os.chmod('start_system.sh', 0o755)

print("\n✅ ORGANISATION TERMINÉE !")
print("\n📋 Commandes disponibles:")
print("  python3 menu_principal.py   # Menu principal")
print("  bash start_system.sh        # Voir le résumé")
print("  ls AGENTS/                  # Voir vos agents IA")
print("  ls APIS/                    # Voir vos APIs")
print("\n🎯 Pour commencer: python3 menu_principal.py")
EOF
