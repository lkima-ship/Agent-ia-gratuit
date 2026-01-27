#!/usr/bin/env python3
# organiseur_complet.py

import os
import shutil
import subprocess
import sys
from datetime import datetime
import glob

class OrganisateurFichiers:
    def __init__(self):
        self.categories = {
            'agents': [
                'agent', 'hub_agents', 'suite_agents', 'verifier_agents',
                'tous_les_agents', 'index_agents', 'sync_agents',
                'agent_ia', 'agent_web', 'agent_analyse'
            ],
            'apis': [
                'api', 'simple_api', 'mini_api', 'debug_api', 'web_dashboard',
                'test_api', 'start_api', 'quick_api', 'rapport_web'
            ],
            'scripts': [
                '.sh', 'start_', 'install_', 'check_', 'backup_',
                'test_', 'menu_', 'dash', 'organise', 'reparer',
                'fix_', 'create_', 'diagnostic'
            ],
            'projets': [
                'projet', 'project', 'flask', 'ecommerce', 'boutique',
                'models', 'configs', 'requirements'
            ],
            'web': [
                '.html', '.htm', 'index', 'boutique', 'shop', 'dashboard'
            ],
            'tests': [
                'test_', 'test.', 'debug', 'verifier'
            ],
            'data': [
                '.db', '.log', '.txt', 'data', 'logs'
            ],
            'systeme': [
                'venv', 'temp', 'sites', 'mes_sites'
            ]
        }
        
    def analyser_fichiers(self):
        """Analyse tous les fichiers du répertoire courant"""
        fichiers = os.listdir('.')
        resultats = {}
        
        for fichier in fichiers:
            if os.path.isfile(fichier):
                categorie = self.determiner_categorie(fichier)
                if categorie not in resultats:
                    resultats[categorie] = []
                resultats[categorie].append(fichier)
        
        return resultats
    
    def determiner_categorie(self, fichier):
        """Détermine la catégorie d'un fichier"""
        nom_lower = fichier.lower()
        
        for categorie, mots_cles in self.categories.items():
            for mot_cle in mots_cles:
                if mot_cle.lower() in nom_lower or fichier.endswith(mot_cle):
                    return categorie
        
        # Vérifier par extension
        if fichier.endswith('.py'):
            return 'scripts_python'
        elif fichier.endswith(('.sh', '.bash')):
            return 'scripts'
        elif fichier.endswith(('.html', '.htm', '.css', '.js')):
            return 'web'
        elif fichier.endswith(('.json', '.yaml', '.yml', '.ini', '.cfg')):
            return 'configs'
        elif fichier.endswith(('.log', '.txt', '.md', '.rst')):
            return 'docs'
        elif fichier.endswith(('.db', '.sqlite', '.csv', '.xlsx')):
            return 'data'
        
        return 'divers'
    
    def creer_structure(self):
        """Crée la structure de dossiers"""
        dossiers = [
            'agents',
            'apis',
            'scripts',
            'scripts_python',
            'projets',
            'web',
            'tests',
            'data',
            'configs',
            'docs',
            'logs',
            'backups',
            'divers'
        ]
        
        for dossier in dossiers:
            if not os.path.exists(dossier):
                os.makedirs(dossier)
                print(f"✓ Créé dossier: {dossier}")
    
    def organiser_fichiers(self):
        """Organise les fichiers dans les dossiers appropriés"""
        fichiers = [f for f in os.listdir('.') if os.path.isfile(f)]
        deplaces = 0
        
        for fichier in fichiers:
            if fichier == __file__:
                continue
                
            categorie = self.determiner_categorie(fichier)
            dossier_cible = categorie
            
            # Déplacer le fichier
            try:
                shutil.move(fichier, os.path.join(dossier_cible, fichier))
                print(f"✓ Déplacé: {fichier} -> {dossier_cible}/")
                deplaces += 1
            except Exception as e:
                print(f"✗ Erreur avec {fichier}: {e}")
        
        print(f"\n✅ {deplaces} fichiers organisés avec succès!")
    
    def creer_menu_principal(self):
        """Crée un menu principal pour accéder à toutes les fonctionnalités"""
        menu_content = '''#!/usr/bin/env python3
# menu_master.py - Menu principal pour tous les projets

import os
import subprocess
import sys
import webbrowser
from datetime import datetime

class MenuMaster:
    def __init__(self):
        self.projets = self.detecter_projets()
        self.agents = self.detecter_agents()
        self.apis = self.detecter_apis()
        
    def detecter_projets(self):
        return {
            'projet_ia_avance': 'Projet IA Avancé',
            'flask-iphone-app': 'Application Flask iPhone',
            'ecommerce_complet': 'Boutique e-commerce',
            'ai_agents_project': 'Projet Agents IA'
        }
    
    def detecter_agents(self):
        agents = {}
        if os.path.exists('agents'):
            for fichier in os.listdir('agents'):
                if fichier.endswith('.py') and 'agent' in fichier.lower():
                    nom = fichier.replace('.py', '').replace('_', ' ').title()
                    agents[fichier] = nom
        return agents
    
    def detecter_apis(self):
        apis = {}
        if os.path.exists('apis'):
            for fichier in os.listdir('apis'):
                if fichier.endswith('.py') and ('api' in fichier.lower() or 'web' in fichier.lower()):
                    nom = fichier.replace('.py', '').replace('_', ' ').title()
                    apis[fichier] = nom
        return apis
    
    def afficher_menu(self):
        while True:
            print("\\n" + "="*60)
            print("MENU MASTER - SYSTÈME COMPLET")
            print("="*60)
            print("1. 🚀 Démarrer l'écosystème complet")
            print("2. 🤖 Agents IA")
            print("3. 🌐 APIs & Serveurs Web")
            print("4. 🛠️  Scripts & Outils")
            print("5. 📊 Tests & Diagnostics")
            print("6. 📁 Gestion des Projets")
            print("7. 🔧 Organisation des fichiers")
            print("8. 📊 Statut du système")
            print("0. ❌ Quitter")
            print("="*60)
            
            choix = input("\\n👉 Votre choix: ").strip()
            
            if choix == '1':
                self.demarrer_ecosysteme()
            elif choix == '2':
                self.menu_agents()
            elif choix == '3':
                self.menu_apis()
            elif choix == '4':
                self.menu_scripts()
            elif choix == '5':
                self.menu_tests()
            elif choix == '6':
                self.menu_projets()
            elif choix == '7':
                self.organiser_fichiers()
            elif choix == '8':
                self.afficher_statut()
            elif choix == '0':
                print("\\n👋 Au revoir!")
                break
            else:
                print("\\n❌ Choix invalide!")
    
    def demarrer_ecosysteme(self):
        print("\\n🚀 Démarrage de l'écosystème complet...")
        scripts = [
            'scripts/start_all.sh',
            'scripts/start_ecosystem.sh',
            'scripts/start_ai.sh',
            'scripts/start_api.sh'
        ]
        
        for script in scripts:
            if os.path.exists(script):
                print(f"▶  Exécution: {script}")
                try:
                    subprocess.run(['bash', script], check=True)
                except:
                    print(f"⚠  Échec: {script}")
    
    def menu_agents(self):
        print("\\n" + "="*60)
        print("🤖 MENU AGENTS IA")
        print("="*60)
        
        if not self.agents:
            print("Aucun agent trouvé dans le dossier 'agents/'")
            return
            
        for i, (fichier, nom) in enumerate(self.agents.items(), 1):
            print(f"{i}. {nom} ({fichier})")
        
        print(f"{len(self.agents)+1}. 📊 Exécuter tous les agents")
        print(f"{len(self.agents)+2}. 🔙 Retour")
        
        choix = input("\\n👉 Choisir un agent: ").strip()
        
        if choix.isdigit():
            idx = int(choix) - 1
            if 0 <= idx < len(self.agents):
                fichier = list(self.agents.keys())[idx]
                self.executer_agent(fichier)
            elif idx == len(self.agents):
                self.executer_tous_agents()
    
    def executer_agent(self, fichier_agent):
        chemin = os.path.join('agents', fichier_agent)
        if os.path.exists(chemin):
            print(f"\\n▶  Exécution de {fichier_agent}...")
            subprocess.run([sys.executable, chemin])
        else:
            print(f"❌ Fichier non trouvé: {chemin}")
    
    def executer_tous_agents(self):
        print("\\n▶  Exécution de tous les agents...")
        for fichier in self.agents:
            self.executer_agent(fichier)
    
    def menu_apis(self):
        print("\\n" + "="*60)
        print("🌐 MENU APIS & SERVEURS")
        print("="*60)
        
        if not self.apis:
            print("Aucune API trouvée dans le dossier 'apis/'")
            return
            
        for i, (fichier, nom) in enumerate(self.apis.items(), 1):
            print(f"{i}. {nom} ({fichier})")
        
        print(f"{len(self.apis)+1}. 🌐 Démarrer toutes les APIs")
        print(f"{len(self.apis)+2}. 📊 Vérifier les ports")
        print(f"{len(self.apis)+3}. 🔙 Retour")
    
    def menu_scripts(self):
        print("\\n" + "="*60)
        print("🛠️  MENU SCRIPTS & OUTILS")
        print("="*60)
        
        if os.path.exists('scripts'):
            scripts = [f for f in os.listdir('scripts') if f.endswith('.sh')]
            for i, script in enumerate(scripts, 1):
                print(f"{i}. {script}")
            
            if scripts:
                choix = input("\\n👉 Choisir un script: ").strip()
                if choix.isdigit():
                    idx = int(choix) - 1
                    if 0 <= idx < len(scripts):
                        self.executer_script(scripts[idx])
    
    def executer_script(self, nom_script):
        chemin = os.path.join('scripts', nom_script)
        if os.path.exists(chemin):
            print(f"\\n▶  Exécution: {nom_script}")
            os.chmod(chemin, 0o755)
            subprocess.run(['bash', chemin])
    
    def menu_tests(self):
        print("\\n" + "="*60)
        print("📊 MENU TESTS & DIAGNOSTICS")
        print("="*60)
        
        tests = [
            ('test_api_complete.sh', 'Tests API complets'),
            ('test_dashboard.sh', 'Tests Dashboard'),
            ('test_simple.py', 'Tests simples Python'),
            ('verifier_agents.sh', 'Vérifier agents')
        ]
        
        for i, (fichier, desc) in enumerate(tests, 1):
            print(f"{i}. {desc} ({fichier})")
    
    def menu_projets(self):
        print("\\n" + "="*60)
        print("📁 MENU PROJETS")
        print("="*60)
        
        for i, (dossier, nom) in enumerate(self.projets.items(), 1):
            existe = "✅" if os.path.exists(dossier) else "❌"
            print(f"{i}. {existe} {nom}")
    
    def organiser_fichiers(self):
        print("\\n🔄 Organisation des fichiers...")
        subprocess.run([sys.executable, 'organiseur_complet.py'])
    
    def afficher_statut(self):
        print("\\n" + "="*60)
        print("📊 STATUT DU SYSTÈME")
        print("="*60)
        
        # Agents
        agents_count = len([f for f in os.listdir('.') if 'agent' in f.lower()]) if os.path.exists('.') else 0
        print(f"🤖 Agents: {agents_count} trouvés")
        
        # APIs
        apis_count = len([f for f in os.listdir('.') if 'api' in f.lower()]) if os.path.exists('.') else 0
        print(f"🌐 APIs: {apis_count} trouvées")
        
        # Scripts
        scripts_count = len([f for f in os.listdir('.') if f.endswith('.sh')]) if os.path.exists('.') else 0
        print(f"🛠️  Scripts: {scripts_count} trouvés")
        
        # Projets
        projets = ['projet_ia_avance', 'flask-iphone-app', 'ecommerce_complet']
        projets_count = sum(1 for p in projets if os.path.exists(p))
        print(f"📁 Projets: {projets_count}/{len(projets)}")
        
        # Espace disque
        import shutil
        total, used, free = shutil.disk_usage(".")
        print(f"💾 Espace: {used // (2**30)} Go utilisé, {free // (2**30)} Go libre")

if __name__ == "__main__":
    menu = MenuMaster()
    menu.afficher_menu()
'''
        
        with open('menu_master.py', 'w', encoding='utf-8') as f:
            f.write(menu_content)
        
        # Rendre exécutable
        os.chmod('menu_master.py', 0o755)
        print("✅ Menu principal créé: menu_master.py")
    
    def creer_agent_analyse(self):
        """Crée un agent d'analyse de données"""
        agent_content = '''#!/usr/bin/env python3
# agent_analyse_donnees.py - Agent d'analyse avancé

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json
import os

class AgentAnalyse:
    def __init__(self):
        self.dossiers_analyse = ['data', 'logs', '.']
        self.resultats = {}
    
    def analyser_structure(self):
        """Analyse la structure des fichiers"""
        print("📊 Analyse de la structure des fichiers...")
        
        fichiers = []
        for dossier in self.dossiers_analyse:
            if os.path.exists(dossier):
                for root, dirs, files in os.walk(dossier):
                    for file in files:
                        chemin = os.path.join(root, file)
                        taille = os.path.getsize(chemin)
                        extension = os.path.splitext(file)[1]
                        
                        fichiers.append({
                            'nom': file,
                            'chemin': chemin,
                            'taille': taille,
                            'extension': extension,
                            'dossier': dossier
                        })
        
        if fichiers:
            df = pd.DataFrame(fichiers)
            print(f"📁 {len(fichiers)} fichiers analysés")
            
            # Analyse par extension
            par_extension = df.groupby('extension').agg({
                'nom': 'count',
                'taille': 'sum'
            }).rename(columns={'nom': 'nombre', 'taille': 'taille_totale'})
            
            print("\\n📈 Répartition par extension:")
            print(par_extension)
            
            # Sauvegarder les résultats
            self.resultats['structure'] = {
                'total_fichiers': len(fichiers),
                'par_extension': par_extension.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
            
            return df
        return None
    
    def analyser_logs(self):
        """Analyse les fichiers logs"""
        print("📝 Analyse des fichiers logs...")
        
        logs_trouves = []
        for dossier in self.dossiers_analyse:
            if os.path.exists(dossier):
                for root, dirs, files in os.walk(dossier):
                    for file in files:
                        if file.endswith('.log'):
                            chemin = os.path.join(root, file)
                            logs_trouves.append(chemin)
        
        print(f"📄 {len(logs_trouves)} fichiers log trouvés")
        
        for log in logs_trouves[:5]:  # Analyser les 5 premiers
            try:
                with open(log, 'r', encoding='utf-8', errors='ignore') as f:
                    lignes = f.readlines()
                    print(f"  {log}: {len(lignes)} lignes")
            except:
                print(f"  {log}: erreur de lecture")
    
    def generer_rapport(self):
        """Génère un rapport complet"""
        print("\\n📋 Génération du rapport...")
        
        rapport = {
            'timestamp': datetime.now().isoformat(),
            'resultats': self.resultats,
            'statistiques': {
                'dossiers_analyses': self.dossiers_analyse,
                'heure_analyse': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        }
        
        # Sauvegarder le rapport
        with open('rapport_analyse.json', 'w', encoding='utf-8') as f:
            json.dump(rapport, f, indent=2, ensure_ascii=False)
        
        print("✅ Rapport sauvegardé: rapport_analyse.json")
        
        # Créer un résumé
        self.creer_resume(rapport)
    
    def creer_resume(self, rapport):
        """Crée un résumé visuel"""
        print("\\n📊 Création du résumé visuel...")
        
        # Exemple de graphique (si matplotlib disponible)
        try:
            if 'structure' in rapport['resultats']:
                data = rapport['resultats']['structure']['par_extension']
                
                extensions = list(data['nombre'].keys())
                nombres = list(data['nombre'].values())
                
                plt.figure(figsize=(10, 6))
                plt.bar(extensions, nombres)
                plt.title('Répartition des fichiers par extension')
                plt.xlabel('Extension')
                plt.ylabel('Nombre de fichiers')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig('analyse_extensions.png')
                print("✅ Graphique sauvegardé: analyse_extensions.png")
        except Exception as e:
            print(f"⚠  Impossible de créer le graphique: {e}")
    
    def executer(self):
        """Exécute l'analyse complète"""
        print("="*60)
        print("AGENT D'ANALYSE DE DONNÉES")
        print("="*60)
        
        self.analyser_structure()
        self.analyser_logs()
        self.generer_rapport()
        
        print("\\n" + "="*60)
        print("✅ Analyse terminée avec succès!")
        print("="*60)

if __name__ == "__main__":
    agent = AgentAnalyse()
    agent.executer()
'''
        
        with open('agent_analyse_donnees.py', 'w', encoding='utf-8') as f:
            f.write(agent_content)
        
        os.chmod('agent_analyse_donnees.py', 0o755)
        print("✅ Agent d'analyse créé: agent_analyse_donnees.py")
    
    def verifier_systeme(self):
        """Vérifie l'état du système et les dépendances"""
        print("\n" + "="*60)
        print("🔍 VÉRIFICATION DU SYSTÈME")
        print("="*60)
        
        # Vérifier Python
        try:
            import pandas
            print("✅ pandas installé")
        except:
            print("❌ pandas non installé")
        
        try:
            import flask
            print("✅ Flask installé")
        except:
            print("❌ Flask non installé")
        
        # Vérifier fichiers importants
        fichiers_importants = [
            'requirements.txt',
            'menu_master.py',
            'agent_analyse_donnees.py'
        ]
        
        for fichier in fichiers_importants:
            if os.path.exists(fichier):
                print(f"✅ {fichier} présent")
            else:
                print(f"❌ {fichier} manquant")
        
        print("\n✅ Vérification terminée!")

def main():
    print("🚀 ORGANISATEUR COMPLET DE PROJETS")
    print("="*60)
    
    organisateur = OrganisateurFichiers()
    
    # 1. Analyser les fichiers
    print("\n📊 Analyse des fichiers en cours...")
    analyse = organisateur.analyser_fichiers()
    
    for categorie, fichiers in analyse.items():
        print(f"  {categorie}: {len(fichiers)} fichiers")
    
    # 2. Créer la structure
    print("\n📁 Création de la structure...")
    organisateur.creer_structure()
    
    # 3. Organiser les fichiers
    print("\n🔄 Organisation des fichiers...")
    organisateur.organiser_fichiers()
    
    # 4. Créer le menu principal
    print("\n📝 Création du menu principal...")
    organisateur.creer_menu_principal()
    
    # 5. Créer l'agent d'analyse
    print("\n🤖 Création de l'agent d'analyse...")
    organisateur.creer_agent_analyse()
    
    # 6. Vérifier le système
    organisateur.verifier_systeme()
    
    print("\n" + "="*60)
    print("🎉 ORGANISATION TERMINÉE AVEC SUCCÈS!")
    print("="*60)
    print("\nCommandes disponibles:")
    print("  python3 menu_master.py     - Menu principal")
    print("  python3 agent_analyse_donnees.py - Agent d'analyse")
    print("  python3 organiseur_complet.py    - Réorganiser")
    print("\nProchaine étape: exécutez 'python3 menu_master.py'")

if __name__ == "__main__":
    main()
