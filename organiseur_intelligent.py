cat > organiseur_intelligent.py << 'EOF'
#!/usr/bin/env python3
# organiseur_intelligent.py - Organisation complète

import os
import shutil
import subprocess
import json
from datetime import datetime
import sys

class OrganisateurIntelligent:
    def __init__(self):
        self.structure = {
            'agents_ia': [
                'agent_ia', 'agent_web', 'agent_analyse', 'agent_cognitif',
                'agent_dashboard', 'agent_surveillance', 'ia_agent', 'hub_agents'
            ],
            'apis_serveurs': [
                'api_', 'server', 'flask', 'app', 'web_dashboard',
                'web_interface', 'rest', 'control_panel', 'simple_backup'
            ],
            'scripts': [
                '.sh', 'start_', 'install_', 'check_', 'launch_',
                'manage_', 'control_', 'test_', 'fix_', 'setup',
                'run_', 'verifier', 'quick_'
            ],
            'projets': [
                'projet', 'project', 'flask-', 'ecommerce', 'boutique',
                'docker', 'src/', 'config/', 'requirements.txt'
            ],
            'web': [
                '.html', '.htm', 'index', 'dashboard', 'interface'
            ],
            'tests': [
                'test_', 'debug_', 'check_', 'verifier'
            ],
            'configs': [
                '.json', '.yaml', '.yml', '.ini', '.cfg',
                'config', 'settings', '.env'
            ],
            'docs': [
                '.md', '.txt', 'README', 'LICENSE', 'lisezmoi'
            ],
            'data': [
                '.db', '.log', '.csv', '.xlsx', 'data/'
            ],
            'divers': []  # Tout le reste
        }
        
        self.rapport = {
            'date': datetime.now().isoformat(),
            'fichiers_deplaces': 0,
            'erreurs': [],
            'structure_creer': []
        }
    
    def analyser_arborescence(self, chemin='.'):
        """Analyse complète de l'arborescence"""
        print(f"\n🔍 Analyse de: {os.path.abspath(chemin)}")
        
        total_fichiers = 0
        total_dossiers = 0
        
        for root, dirs, files in os.walk(chemin):
            total_dossiers += len(dirs)
            total_fichiers += len(files)
            
            print(f"\n📁 {root}/")
            for f in files[:10]:  # Afficher les 10 premiers fichiers
                print(f"   📄 {f}")
            if len(files) > 10:
                print(f"   ... et {len(files) - 10} autres")
        
        print(f"\n📊 Totaux: {total_fichiers} fichiers, {total_dossiers} dossiers")
        return total_fichiers, total_dossiers
    
    def creer_structure_complete(self):
        """Crée la structure de dossiers complète"""
        print("\n🏗️  Création de la structure...")
        
        structure = [
            'systeme_ia/agents',
            'systeme_ia/apis',
            'systeme_ia/serveurs',
            'systeme_ia/scripts',
            'systeme_ia/interfaces',
            'systeme_ia/data',
            'systeme_ia/logs',
            'systeme_ia/configs',
            
            'projets/flask',
            'projets/web',
            'projets/api',
            'projets/docker',
            
            'scripts/installation',
            'scripts/demarrage',
            'scripts/maintenance',
            'scripts/test',
            
            'web/templates',
            'web/static',
            'web/assets',
            
            'tests/unitaires',
            'tests/integration',
            'tests/api',
            
            'data/bases',
            'data/logs',
            'data/cache',
            
            'docs',
            'backups',
            'temp'
        ]
        
        for dossier in structure:
            if not os.path.exists(dossier):
                os.makedirs(dossier, exist_ok=True)
                self.rapport['structure_creer'].append(dossier)
                print(f"✅ {dossier}")
    
    def determiner_destination(self, fichier, chemin_complet):
        """Détermine où placer un fichier"""
        nom = fichier.lower()
        
        # Par extension d'abord
        if fichier.endswith('.py'):
            if any(mot in nom for mot in ['agent', 'ia', 'cognitif', 'analyse']):
                return 'systeme_ia/agents'
            elif any(mot in nom for mot in ['api', 'server', 'flask', 'app', 'web']):
                return 'systeme_ia/apis'
            elif any(mot in nom for mot in ['test', 'debug']):
                return 'tests/unitaires'
            elif any(mot in nom for mot in ['config', 'settings']):
                return 'systeme_ia/configs'
            else:
                return 'scripts/maintenance'
        
        elif fichier.endswith('.sh'):
            if any(mot in nom for mot in ['start', 'launch', 'run']):
                return 'scripts/demarrage'
            elif any(mot in nom for mot in ['install', 'setup']):
                return 'scripts/installation'
            elif any(mot in nom for mot in ['check', 'test', 'verifier']):
                return 'scripts/test'
            else:
                return 'scripts/maintenance'
        
        elif fichier.endswith(('.html', '.htm')):
            return 'web/templates'
        
        elif fichier.endswith(('.css', '.js', '.png', '.jpg', '.svg')):
            return 'web/static'
        
        elif fichier.endswith(('.json', '.yaml', '.yml', '.ini', '.cfg')):
            return 'systeme_ia/configs'
        
        elif fichier.endswith(('.db', '.sqlite', '.csv')):
            return 'data/bases'
        
        elif fichier.endswith(('.log', '.txt')):
            return 'data/logs'
        
        elif fichier.endswith(('.md', '.rst')):
            return 'docs'
        
        # Par nom
        elif any(mot in nom for mot in ['docker', 'compose']):
            return 'projets/docker'
        
        elif 'requirements' in nom:
            return 'projets/flask'
        
        elif 'agent' in nom:
            return 'systeme_ia/agents'
        
        elif 'api' in nom:
            return 'systeme_ia/apis'
        
        elif 'menu' in nom:
            return 'systeme_ia/interfaces'
        
        elif 'test' in nom:
            return 'tests/integration'
        
        else:
            return 'divers'
    
    def organiser_fichiers(self, racine='.'):
        """Organise tous les fichiers"""
        print("\n🔄 Organisation des fichiers...")
        
        fichiers_a_traiter = []
        
        # Collecter tous les fichiers
        for root, dirs, files in os.walk(racine):
            # Ignorer certains dossiers
            if any(ignore in root for ignore in ['systeme_ia', 'projets', 'scripts', 'web', 'tests', 'data', 'docs', 'backups', 'temp', 'divers']):
                continue
            
            for fichier in files:
                if fichier == os.path.basename(__file__):
                    continue
                
                chemin_complet = os.path.join(root, fichier)
                fichiers_a_traiter.append((chemin_complet, fichier, root))
        
        print(f"📦 {len(fichiers_a_traiter)} fichiers à organiser")
        
        # Traiter chaque fichier
        for chemin_complet, fichier, origine in fichiers_a_traiter:
            try:
                destination = self.determiner_destination(fichier, chemin_complet)
                dest_path = os.path.join(destination, fichier)
                
                # Éviter les collisions
                if os.path.exists(dest_path):
                    # Ajouter un suffixe numérique
                    base, ext = os.path.splitext(fichier)
                    counter = 1
                    while os.path.exists(dest_path):
                        nouveau_nom = f"{base}_{counter}{ext}"
                        dest_path = os.path.join(destination, nouveau_nom)
                        counter += 1
                
                # Déplacer le fichier
                shutil.move(chemin_complet, dest_path)
                self.rapport['fichiers_deplaces'] += 1
                
                rel_origine = os.path.relpath(origine, racine)
                rel_dest = os.path.relpath(destination, racine)
                print(f"✓ {rel_origine}/{fichier} → {rel_dest}/")
                
            except Exception as e:
                erreur = f"{fichier}: {str(e)}"
                self.rapport['erreurs'].append(erreur)
                print(f"✗ {erreur}")
    
    def creer_systeme_complet(self):
        """Crée tous les fichiers système nécessaires"""
        print("\n⚙️  Création du système complet...")
        
        # 1. Menu principal avancé
        menu_content = '''#!/usr/bin/env python3
# systeme_menu.py - Menu principal du système IA

import os
import sys
import subprocess
import webbrowser
from datetime import datetime

class SystemeMenu:
    def __init__(self):
        self.version = "2.0.0"
        self.chemin_base = os.path.dirname(os.path.abspath(__file__))
    
    def afficher_en_tete(self):
        print("\\n" + "="*70)
        print("🤖 SYSTÈME IA COMPLET - MENU PRINCIPAL")
        print("="*70)
        print(f"Version: {self.version} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70)
    
    def afficher_menu(self):
        self.afficher_en_tete()
        
        options = [
            "🚀 DÉMARRAGE RAPIDE",
            "🤖 AGENTS IA",
            "🌐 APIS & SERVEURS",
            "🛠️  SCRIPTS & OUTILS",
            "📁 PROJETS",
            "📊 TABLEAU DE BORD",
            "⚙️  CONFIGURATION",
            "🧪 TESTS",
            "🔧 MAINTENANCE",
            "❌ QUITTER"
        ]
        
        for i, option in enumerate(options, 1):
            print(f"{i:2}. {option}")
        
        print("="*70)
    
    def executer_commande(self, commande):
        """Exécute une commande système"""
        try:
            if commande.startswith("cd "):
                os.chdir(commande[3:])
                print(f"📁 Répertoire: {os.getcwd()}")
            else:
                result = subprocess.run(commande, shell=True, capture_output=True, text=True)
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(f"⚠  {result.stderr}")
        except Exception as e:
            print(f"❌ Erreur: {e}")
    
    def lancer_agent(self, nom_agent):
        """Lance un agent IA"""
        chemin = f"systeme_ia/agents/{nom_agent}"
        if os.path.exists(chemin):
            print(f"▶  Lancement: {nom_agent}")
            self.executer_commande(f"python3 {chemin}")
        else:
            print(f"❌ Agent non trouvé: {chemin}")
    
    def demarrer_api(self, nom_api):
        """Démarre une API"""
        chemin = f"systeme_ia/apis/{nom_api}"
        if os.path.exists(chemin):
            print(f"🌐 Démarrage API: {nom_api}")
            print(f"   Accès: http://localhost:5000")
            self.executer_commande(f"python3 {chemin} &")
        else:
            print(f"❌ API non trouvée: {chemin}")
    
    def menu_agents(self):
        """Menu des agents IA"""
        print("\\n🤖 MENU AGENTS IA")
        print("-"*40)
        
        agents = []
        if os.path.exists("systeme_ia/agents"):
            agents = [f for f in os.listdir("systeme_ia/agents") if f.endswith('.py')]
        
        if not agents:
            print("Aucun agent trouvé")
            return
        
        for i, agent in enumerate(agents[:10], 1):
            print(f"{i}. {agent}")
        
        if len(agents) > 10:
            print(f"... et {len(agents) - 10} autres")
        
        print("0. Retour")
        
        choix = input("\\n👉 Choix: ")
        if choix.isdigit():
            idx = int(choix) - 1
            if 0 <= idx < len(agents):
                self.lancer_agent(agents[idx])
    
    def menu_apis(self):
        """Menu des APIs"""
        print("\\n🌐 MENU APIS & SERVEURS")
        print("-"*40)
        
        apis = []
        if os.path.exists("systeme_ia/apis"):
            apis = [f for f in os.listdir("systeme_ia/apis") if f.endswith('.py')]
        
        if not apis:
            print("Aucune API trouvée")
            return
        
        for i, api in enumerate(apis[:10], 1):
            print(f"{i}. {api}")
        
        print("A. Démarrer toutes les APIs")
        print("0. Retour")
        
        choix = input("\\n👉 Choix: ")
        if choix == "A":
            for api in apis:
                self.demarrer_api(api)
        elif choix.isdigit():
            idx = int(choix) - 1
            if 0 <= idx < len(apis):
                self.demarrer_api(apis[idx])
    
    def menu_scripts(self):
        """Menu des scripts"""
        print("\\n🛠️  MENU SCRIPTS")
        print("-"*40)
        
        categories = ['demarrage', 'installation', 'maintenance', 'test']
        for i, cat in enumerate(categories, 1):
            chemin = f"scripts/{cat}"
            if os.path.exists(chemin):
                nb = len([f for f in os.listdir(chemin) if f.endswith('.sh')])
                print(f"{i}. {cat.capitalize()} ({nb} scripts)")
        
        print("0. Retour")
        
        choix = input("\\n👉 Choix: ")
        if choix == "1":
            self.lister_scripts("scripts/demarrage")
        elif choix == "2":
            self.lister_scripts("scripts/installation")
    
    def lister_scripts(self, dossier):
        """Liste les scripts d'un dossier"""
        if os.path.exists(dossier):
            scripts = [f for f in os.listdir(dossier) if f.endswith('.sh')]
            for i, script in enumerate(scripts, 1):
                print(f"{i}. {script}")
            
            if scripts:
                choix = input("\\nExécuter un script (numéro): ")
                if choix.isdigit():
                    idx = int(choix) - 1
                    if 0 <= idx < len(scripts):
                        self.executer_commande(f"bash {dossier}/{scripts[idx]}")
    
    def afficher_statistiques(self):
        """Affiche les statistiques du système"""
        print("\\n📊 STATISTIQUES DU SYSTÈME")
        print("-"*40)
        
        dossiers = {
            'Agents IA': 'systeme_ia/agents',
            'APIs': 'systeme_ia/apis',
            'Scripts': 'scripts',
            'Projets': 'projets',
            'Tests': 'tests',
            'Documentation': 'docs'
        }
        
        for nom, chemin in dossiers.items():
            if os.path.exists(chemin):
                if os.path.isdir(chemin):
                    fichiers = len([f for f in os.listdir(chemin) if os.path.isfile(os.path.join(chemin, f))])
                    print(f"📁 {nom}: {fichiers} fichiers")
                else:
                    print(f"📄 {nom}: Présent")
            else:
                print(f"❌ {nom}: Manquant")
    
    def executer(self):
        """Exécute le menu principal"""
        while True:
            self.afficher_menu()
            choix = input("\\n👉 Votre choix (1-10): ").strip()
            
            if choix == "1":
                print("\\n🚀 DÉMARRAGE RAPIDE...")
                self.executer_commande("bash scripts/demarrage/start_all.sh")
            
            elif choix == "2":
                self.menu_agents()
            
            elif choix == "3":
                self.menu_apis()
            
            elif choix == "4":
                self.menu_scripts()
            
            elif choix == "5":
                print("\\n📁 PROJETS...")
                self.executer_commande("ls -la projets/")
            
            elif choix == "6":
                print("\\n📊 TABLEAU DE BORD...")
                self.afficher_statistiques()
            
            elif choix == "7":
                print("\\n⚙️  CONFIGURATION...")
                self.executer_commande("ls -la systeme_ia/configs/")
            
            elif choix == "8":
                print("\\n🧪 TESTS...")
                self.executer_commande("bash scripts/test/run_tests.sh")
            
            elif choix == "9":
                print("\\n🔧 MAINTENANCE...")
                self.executer_commande("bash scripts/maintenance/cleanup.sh")
            
            elif choix == "10":
                print("\\n👋 Au revoir!")
                sys.exit(0)
            
            else:
                print("\\n❌ Choix invalide!")
            
            input("\\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        menu = SystemeMenu()
        menu.executer()
    except KeyboardInterrupt:
        print("\\n\\n👋 Interrompu par l'utilisateur")
        sys.exit(0)
'''
        
        with open('systeme_menu.py', 'w', encoding='utf-8') as f:
            f.write(menu_content)
        
        # 2. Script de démarrage complet
        start_content = '''#!/bin/bash
# start_all.sh - Démarrage du système complet

echo "=========================================="
echo "🚀 SYSTÈME IA - DÉMARRAGE COMPLET"
echo "=========================================="
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Vérifier l'organisation
info "Vérification de la structure..."
if [ ! -d "systeme_ia" ]; then
    warning "Structure non organisée. Exécution de l'organisateur..."
    python3 organiseur_intelligent.py
fi

# Statistiques
info "Statistiques du système:"
[ -d "systeme_ia/agents" ] && echo "  🤖 Agents: $(ls systeme_ia/agents/*.py 2>/dev/null | wc -l)"
[ -d "systeme_ia/apis" ] && echo "  🌐 APIs: $(ls systeme_ia/apis/*.py 2>/dev/null | wc -l)"
[ -d "scripts/demarrage" ] && echo "  🛠️  Scripts: $(ls scripts/demarrage/*.sh 2>/dev/null | wc -l)"
[ -d "projets" ] && echo "  📁 Projets: $(ls projets/*/ 2>/dev/null | wc -l)"

# Vérifier Python
info "Vérification de Python..."
if command -v python3 &>/dev/null; then
    success "Python3 installé"
else
    error "Python3 non installé"
    exit 1
fi

# Menu interactif
echo ""
success "Système prêt!"
echo ""
echo "Commandes disponibles:"
echo "  1. python3 systeme_menu.py       - Menu principal"
echo "  2. bash scripts/demarrage/start_agents.sh - Démarrer les agents"
echo "  3. bash scripts/demarrage/start_apis.sh   - Démarrer les APIs"
echo "  4. ls systeme_ia/agents/         - Voir les agents"
echo "  5. ls systeme_ia/apis/           - Voir les APIs"
echo ""

read -p "Lancer le menu principal? (o/n) " choix
if [[ $choix == "o" || $choix == "O" ]]; then
    python3 systeme_menu.py
fi

echo ""
echo "=========================================="
echo "✅ DÉMARRAGE TERMINÉ"
echo "=========================================="
'''
        
        os.makedirs('scripts/demarrage', exist_ok=True)
        with open('scripts/demarrage/start_all.sh', 'w', encoding='utf-8') as f:
            f.write(start_content)
        
        # 3. Script de démarrage des agents
        agents_start = '''#!/bin/bash
# start_agents.sh - Démarrage des agents IA

echo "🤖 DÉMARRAGE DES AGENTS IA"
echo "=========================="

if [ ! -d "systeme_ia/agents" ]; then
    echo "❌ Dossier agents non trouvé"
    exit 1
fi

# Liste des agents
agents=$(ls systeme_ia/agents/*.py 2>/dev/null)

if [ -z "$agents" ]; then
    echo "⚠  Aucun agent trouvé"
    exit 0
fi

echo "Agents disponibles:"
for agent in $agents; do
    echo "  📄 $(basename $agent)"
done

echo ""
read -p "Démarrer tous les agents? (o/n) " choix

if [[ $choix == "o" || $choix == "O" ]]; then
    for agent in $agents; do
        agent_name=$(basename $agent)
        echo "▶  Démarrage: $agent_name"
        python3 "$agent" &
        echo "   PID: $!"
    done
    echo ""
    echo "✅ Tous les agents démarrés en arrière-plan"
    echo "📊 Utilisez 'ps aux | grep python' pour voir les processus"
fi
'''
        
        with open('scripts/demarrage/start_agents.sh', 'w', encoding='utf-8') as f:
            f.write(agents_start)
        
        # 4. Fichier de configuration
        config_content = '''{
    "version": "2.0.0",
    "date_organisation": "__DATE__",
    "structure": {
        "agents": "systeme_ia/agents",
        "apis": "systeme_ia/apis",
        "scripts": "scripts",
        "projets": "projets",
        "web": "web",
        "tests": "tests",
        "data": "data",
        "docs": "docs"
    },
    "fichiers_systeme": [
        "systeme_menu.py",
        "organiseur_intelligent.py",
        "scripts/demarrage/start_all.sh",
        "scripts/demarrage/start_agents.sh"
    ]
}
'''
        
        config_content = config_content.replace('__DATE__', datetime.now().isoformat())
        with open('systeme_ia/configs/systeme_config.json', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        # Rendre exécutables
        os.chmod('systeme_menu.py', 0o755)
        os.chmod('scripts/demarrage/start_all.sh', 0o755)
        os.chmod('scripts/demarrage/start_agents.sh', 0o755)
        
        print("✅ Système créé:")
        print("   - systeme_menu.py (Menu principal)")
        print("   - scripts/demarrage/start_all.sh")
        print("   - scripts/demarrage/start_agents.sh")
        print("   - systeme_ia/configs/systeme_config.json")
    
    def generer_rapport(self):
        """Génère un rapport d'organisation"""
        print("\n📋 Génération du rapport...")
        
        rapport_file = f"rapport_organisation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(rapport_file, 'w', encoding='utf-8') as f:
            json.dump(self.rapport, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Rapport sauvegardé: {rapport_file}")
        
        # Afficher le résumé
        print("\n" + "="*60)
        print("📊 RÉSUMÉ DE L'ORGANISATION")
        print("="*60)
        print(f"📅 Date: {self.rapport['date']}")
        print(f"📦 Fichiers déplacés: {self.rapport['fichiers_deplaces']}")
        print(f"🏗️  Dossiers créés: {len(self.rapport['structure_creer'])}")
        print(f"❌ Erreurs: {len(self.rapport['erreurs'])}")
        print("="*60)
    
    def executer(self):
        """Exécute l'organisation complète"""
        print("\n" + "="*60)
        print("🤖 ORGANISATEUR INTELLIGENT - SYSTÈME IA")
        print("="*60)
        
        # 1. Analyse
        self.analyser_arborescence()
        
        # 2. Création structure
        self.creer_structure_complete()
        
        # 3. Organisation
        self.organiser_fichiers()
        
        # 4. Création système
        self.creer_systeme_complet()
        
        # 5. Rapport
        self.generer_rapport()
        
        print("\n🎉 ORGANISATION TERMINÉE AVEC SUCCÈS!")
        print("\n📋 Commandes disponibles:")
        print("  1. python3 systeme_menu.py         - Menu principal")
        print("  2. bash scripts/demarrage/start_all.sh - Tout démarrer")
        print("  3. python3 organiseur_intelligent.py   - Réorganiser")
        print("  4. ls systeme_ia/agents/           - Voir les agents IA")
        print("  5. ls systeme_ia/apis/             - Voir les APIs")
        print("\n🚀 Pour commencer: python3 systeme_menu.py")

def main():
    try:
        organisateur = OrganisateurIntelligent()
        organisateur.executer()
    except KeyboardInterrupt:
        print("\n\n👋 Opération interrompue par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF
