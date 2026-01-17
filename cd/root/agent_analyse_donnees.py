cd /root

# Mettre à jour agent_analyse_donnees.py avec de vraies fonctionnalités
cat > agent_analyse_donnees.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT D'ANALYSE DE DONNÉES AVANCÉ
"""
import json
import csv
import os
import statistics
from datetime import datetime
from collections import Counter

class AnalyseurDonnees:
    def __init__(self):
        self.historique = []
    
    def analyser_csv_complet(self, fichier):
        """Analyse détaillée d'un fichier CSV"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                lignes = list(reader)
            
            if not lignes:
                return {"erreur": "Fichier vide"}
            
            entete = lignes[0]
            donnees = lignes[1:]
            
            # Nettoyer les données vides
            donnees = [ligne for ligne in donnees if ligne and any(cell.strip() for cell in ligne)]
            
            stats = {
                "nom_fichier": os.path.basename(fichier),
                "lignes_total": len(lignes),
                "lignes_donnees": len(donnees),
                "lignes_vides": len(lignes) - 1 - len(donnees),
                "colonnes": len(entete),
                "en_tete": entete,
                "exemple_premiere_ligne": donnees[0] if donnees else [],
                "exemple_derniere_ligne": donnees[-1] if donnees else [],
                "types_donnees": self.determiner_types_colonnes(donnees, entete),
                "statistiques_numeriques": self.calculer_stats_numeriques(donnees, entete)
            }
            
            # Sauvegarder l'analyse
            self.historique.append({
                "type": "csv",
                "fichier": fichier,
                "timestamp": datetime.now().isoformat(),
                "stats": stats
            })
            
            return stats
        except Exception as e:
            return {"erreur": str(e)}
    
    def determiner_types_colonnes(self, donnees, entete):
        """Détermine le type de données de chaque colonne"""
        if not donnees or not entete:
            return {}
        
        types = {}
        for i, colonne in enumerate(entete):
            valeurs = []
            for ligne in donnees:
                if i < len(ligne):
                    valeur = ligne[i].strip()
                    if valeur:
                        valeurs.append(valeur)
            
            if not valeurs:
                types[colonne] = "VIDE"
                continue
            
            # Analyser le type
            est_numerique = 0
            est_date = 0
            est_texte = 0
            
            for valeur in valeurs:
                # Essayer numérique
                try:
                    float(valeur.replace(',', '.'))
                    est_numerique += 1
                except:
                    # Essayer date
                    try:
                        datetime.strptime(valeur, '%Y-%m-%d')
                        est_date += 1
                    except:
                        try:
                            datetime.strptime(valeur, '%d/%m/%Y')
                            est_date += 1
                        except:
                            est_texte += 1
            
            total = est_numerique + est_date + est_texte
            if est_numerique / total > 0.8:
                types[colonne] = "NUMÉRIQUE"
            elif est_date / total > 0.8:
                types[colonne] = "DATE"
            else:
                types[colonne] = "TEXTE"
        
        return types
    
    def calculer_stats_numeriques(self, donnees, entete):
        """Calcule les statistiques pour les colonnes numériques"""
        stats = {}
        
        for i, colonne in enumerate(entete):
            valeurs_numeriques = []
            for ligne in donnees:
                if i < len(ligne):
                    valeur = ligne[i].strip().replace(',', '.')
                    try:
                        num = float(valeur)
                        valeurs_numeriques.append(num)
                    except:
                        pass
            
            if len(valeurs_numeriques) >= 2:
                stats[colonne] = {
                    "count": len(valeurs_numeriques),
                    "moyenne": round(statistics.mean(valeurs_numeriques), 2),
                    "medianne": round(statistics.median(valeurs_numeriques), 2),
                    "min": round(min(valeurs_numeriques), 2),
                    "max": round(max(valeurs_numeriques), 2),
                    "ecart_type": round(statistics.stdev(valeurs_numeriques), 2) if len(valeurs_numeriques) > 1 else 0
                }
        
        return stats
    
    def analyser_json_avance(self, fichier):
        """Analyse avancée d'un fichier JSON"""
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            stats = {
                "nom_fichier": os.path.basename(fichier),
                "taille_octets": os.path.getsize(fichier),
                "structure": self.analyser_structure_json(data),
                "profondeur_max": self.calculer_profondeur(data),
                "nombre_elements": self.compter_elements(data)
            }
            
            # Sauvegarder l'analyse
            self.historique.append({
                "type": "json",
                "fichier": fichier,
                "timestamp": datetime.now().isoformat(),
                "stats": stats
            })
            
            return stats
        except Exception as e:
            return {"erreur": str(e)}
    
    def analyser_structure_json(self, data):
        """Analyse la structure d'un objet JSON"""
        if isinstance(data, dict):
            return {
                "type": "object",
                "cles": list(data.keys()),
                "nombre_cles": len(data),
                "types_valeurs": {k: type(v).__name__ for k, v in data.items()}
            }
        elif isinstance(data, list):
            if data:
                return {
                    "type": "array",
                    "longueur": len(data),
                    "type_elements": type(data[0]).__name__,
                    "exemple_premier": str(data[0])[:100]
                }
            else:
                return {"type": "array", "longueur": 0}
        else:
            return {"type": type(data).__name__, "valeur": str(data)[:100]}
    
    def calculer_profondeur(self, data, profondeur=0):
        """Calcule la profondeur maximale d'un objet JSON"""
        if isinstance(data, dict):
            if data:
                return max(self.calculer_profondeur(v, profondeur + 1) for v in data.values())
            else:
                return profondeur + 1
        elif isinstance(data, list):
            if data:
                return max(self.calculer_profondeur(item, profondeur + 1) for item in data)
            else:
                return profondeur + 1
        else:
            return profondeur
    
    def compter_elements(self, data):
        """Compte le nombre total d'éléments dans un objet JSON"""
        if isinstance(data, dict):
            return sum(self.compter_elements(v) for v in data.values()) + len(data)
        elif isinstance(data, list):
            return sum(self.compter_elements(item) for item in data) + len(data)
        else:
            return 1
    
    def generer_rapport(self, fichier, type_fichier):
        """Génère un rapport d'analyse"""
        if type_fichier == "csv":
            stats = self.analyser_csv_complet(fichier)
        elif type_fichier == "json":
            stats = self.analyser_json_avance(fichier)
        else:
            return {"erreur": "Type de fichier non supporté"}
        
        if "erreur" in stats:
            return stats
        
        # Créer un rapport formaté
        rapport = {
            "fichier": fichier,
            "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "statistiques": stats,
            "recommandations": self.generer_recommandations(stats)
        }
        
        return rapport
    
    def generer_recommandations(self, stats):
        """Génère des recommandations basées sur l'analyse"""
        recommandations = []
        
        if "en_tete" in stats:
            # Pour CSV
            if stats["lignes_vides"] > 0:
                recommandations.append(f"⚠️  {stats['lignes_vides']} lignes vides détectées")
            
            if stats["colonnes"] > 10:
                recommandations.append(f"📊 {stats['colonnes']} colonnes - considérer la normalisation")
            
            if stats["types_donnees"]:
                for colonne, type_donnee in stats["types_donnees"].items():
                    if type_donnee == "NUMÉRIQUE":
                        recommandations.append(f"📈 Colonne '{colonne}' : données numériques - possibilité d'analyse statistique")
        
        return recommandations
    
    def creer_fichier_exemple(self, type_fichier):
        """Crée un fichier d'exemple"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if type_fichier == "csv":
            nom_fichier = f"exemple_donnees_{timestamp}.csv"
            donnees = [
                ["ID", "Nom", "Age", "Ville", "Salaire", "Date_Embauche"],
                ["1", "Alice Dupont", "28", "Paris", "45000", "2020-05-15"],
                ["2", "Bernard Martin", "35", "Lyon", "52000", "2018-11-22"],
                ["3", "Clara Bernard", "42", "Marseille", "61000", "2015-03-10"],
                ["4", "David Petit", "31", "Toulouse", "48000", "2019-08-30"],
                ["5", "Emma Laurent", "26", "Nice", "42000", "2021-01-18"],
                ["6", "François Moreau", "39", "Bordeaux", "55000", "2017-06-25"],
                ["7", "Gisèle Roux", "45", "Lille", "67000", "2014-09-12"],
                ["8", "Henri Leroy", "33", "Strasbourg", "49000", "2019-03-08"],
                ["9", "Isabelle Simon", "29", "Nantes", "46000", "2020-07-19"],
                ["10", "Julien Michel", "37", "Montpellier", "53000", "2018-04-14"]
            ]
            
            with open(nom_fichier, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(donnees)
            
            return nom_fichier
        
        elif type_fichier == "json":
            nom_fichier = f"exemple_donnees_{timestamp}.json"
            donnees = {
                "projet": "Analyse Données IA",
                "version": "2.0",
                "metadata": {
                    "createur": "Agent IA",
                    "date_creation": datetime.now().isoformat(),
                    "type": "exemple"
                },
                "utilisateurs": [
                    {"id": 1, "nom": "Alice", "age": 28, "actif": True, "competences": ["Python", "Data"]},
                    {"id": 2, "nom": "Bob", "age": 35, "actif": True, "competences": ["SQL", "BI"]},
                    {"id": 3, "nom": "Charlie", "age": 42, "actif": False, "competences": ["ML", "Stats"]}
                ],
                "statistiques": {
                    "total_utilisateurs": 3,
                    "age_moyen": 35,
                    "pourcentage_actifs": 66.67
                }
            }
            
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                json.dump(donnees, f, indent=2, ensure_ascii=False)
            
            return nom_fichier
        
        return None

def afficher_menu():
    print("\n" + "="*60)
    print("           📊 AGENT D'ANALYSE DE DONNÉES V2.0")
    print("="*60)
    print("📋 MENU PRINCIPAL :")
    print("1. 🔍 Analyser un fichier CSV")
    print("2. 📄 Analyser un fichier JSON")
    print("3. 📈 Générer un rapport complet")
    print("4. 📝 Créer des fichiers d'exemple")
    print("5. 📜 Voir l'historique des analyses")
    print("6. 💾 Exporter les résultats")
    print("0. 🚪 Quitter")

def main():
    analyseur = AnalyseurDonnees()
    
    print("🚀 LANCEMENT DE L'ANALYSEUR DE DONNÉES AVANCÉ")
    print("Version 2.0 - IA Powered")
    
    while True:
        afficher_menu()
        
        choix = input("\n👉 Votre choix : ")
        
        if choix == "1":
            fichier = input("Chemin du fichier CSV : ").strip()
            if not fichier:
                print("❌ Aucun fichier spécifié")
                continue
            
            if not os.path.exists(fichier):
                print(f"❌ Fichier '{fichier}' non trouvé")
                continue
            
            print(f"\n🔍 Analyse de {fichier}...")
            stats = analyseur.analyser_csv_complet(fichier)
            
            if "erreur" in stats:
                print(f"❌ Erreur : {stats['erreur']}")
            else:
                print(f"\n✅ Analyse terminée !")
                print(f"📁 Fichier : {stats['nom_fichier']}")
                print(f"📊 Structure : {stats['lignes_donnees']} lignes × {stats['colonnes']} colonnes")
                print(f"📝 Lignes vides : {stats.get('lignes_vides', 0)}")
                
                if stats['types_donnees']:
                    print("\n📋 Types de données par colonne :")
                    for colonne, type_donnee in stats['types_donnees'].items():
                        print(f"  • {colonne} : {type_donnee}")
                
                if stats['statistiques_numeriques']:
                    print("\n📈 Statistiques numériques :")
                    for colonne, stats_col in stats['statistiques_numeriques'].items():
                        print(f"  • {colonne} :")
                        print(f"    - Moyenne: {stats_col['moyenne']}")
                        print(f"    - Min/Max: {stats_col['min']}/{stats_col['max']}")
        
        elif choix == "2":
            fichier = input("Chemin du fichier JSON : ").strip()
            if not fichier:
                print("❌ Aucun fichier spécifié")
                continue
            
            if not os.path.exists(fichier):
                print(f"❌ Fichier '{fichier}' non trouvé")
                continue
            
            print(f"\n🔍 Analyse de {fichier}...")
            stats = analyseur.analyser_json_avance(fichier)
            
            if "erreur" in stats:
                print(f"❌ Erreur : {stats['erreur']}")
            else:
                print(f"\n✅ Analyse terminée !")
                print(f"📁 Fichier : {stats['nom_fichier']}")
                print(f"📏 Taille : {stats['taille_octets']} octets")
                print(f"🏗️  Structure : {stats['structure']['type']}")
                
                if stats['structure']['type'] == 'object':
                    print(f"🔑 Clés : {', '.join(stats['structure']['cles'][:5])}...")
                elif stats['structure']['type'] == 'array':
                    print(f"📊 Nombre d'éléments : {stats['structure']['longueur']}")
                
                print(f"📐 Profondeur maximale : {stats['profondeur_max']}")
                print(f"🧮 Nombre total d'éléments : {stats['nombre_elements']}")
        
        elif choix == "3":
            fichier = input("Chemin du fichier : ").strip()
            if not fichier:
                print("❌ Aucun fichier spécifié")
                continue
            
            if not os.path.exists(fichier):
                print(f"❌ Fichier '{fichier}' non trouvé")
                continue
            
            type_fichier = input("Type de fichier (csv/json) : ").lower()
            if type_fichier not in ['csv', 'json']:
                print("❌ Type de fichier invalide")
                continue
            
            print(f"\n📄 Génération du rapport pour {fichier}...")
            rapport = analyseur.generer_rapport(fichier, type_fichier)
            
            if "erreur" in rapport:
                print(f"❌ Erreur : {rapport['erreur']}")
            else:
                print(f"\n📋 RAPPORT D'ANALYSE")
                print("="*40)
                print(f"📁 Fichier : {rapport['fichier']}")
                print(f"📅 Date d'analyse : {rapport['date_analyse']}")
                
                if rapport['recommandations']:
                    print("\n💡 RECOMMANDATIONS :")
                    for rec in rapport['recommandations']:
                        print(f"  • {rec}")
        
        elif choix == "4":
            print("\n📝 CRÉATION DE FICHIERS D'EXEMPLE")
            print("1. CSV (données utilisateurs)")
            print("2. JSON (structure complexe)")
            
            sous_choix = input("Type de fichier : ")
            
            if sous_choix == "1":
                fichier = analyseur.creer_fichier_exemple("csv")
                if fichier:
                    print(f"✅ Fichier CSV créé : {fichier}")
                    print(f"📊 Contient : 10 utilisateurs avec 6 colonnes")
            elif sous_choix == "2":
                fichier = analyseur.creer_fichier_exemple("json")
                if fichier:
                    print(f"✅ Fichier JSON créé : {fichier}")
                    print(f"📊 Structure : objet avec métadonnées et utilisateurs")
            else:
                print("❌ Choix invalide")
        
        elif choix == "5":
            if not analyseur.historique:
                print("\n📭 Historique vide")
            else:
                print(f"\n📜 HISTORIQUE DES ANALYSES ({len(analyseur.historique)})")
                for i, analyse in enumerate(analyseur.historique[-5:], 1):
                    date = datetime.fromisoformat(analyse['timestamp']).strftime('%H:%M')
                    print(f"{i}. [{date}] {analyse['type'].upper()} : {analyse['fichier']}")
        
        elif choix == "6":
            if not analyseur.historique:
                print("❌ Aucune analyse à exporter")
            else:
                nom_fichier = f"export_analyses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(nom_fichier, 'w', encoding='utf-8') as f:
                    json.dump(analyseur.historique, f, indent=2, ensure_ascii=False)
                print(f"✅ Données exportées dans {nom_fichier}")
        
        elif choix == "0":
            print("\n👋 Au revoir ! Agent d'analyse terminé.")
            break
        
        else:
            print("❌ Choix invalide")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF

# Tester l'agent amélioré
python3 agent_analyse_donnees.py
