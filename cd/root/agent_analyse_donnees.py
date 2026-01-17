cat > agent_analyse_donnees.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT D'ANALYSE DE DONNÉES
"""
import json
import csv
import statistics
from datetime import datetime
import os

class AgentAnalyseDonnees:
    def analyser_csv(self, fichier):
        """Analyse un fichier CSV"""
        try:
            with open(fichier, 'r') as f:
                reader = csv.reader(f)
                lignes = list(reader)
            
            if not lignes:
                return {"erreur": "Fichier vide"}
            
            # Analyse basique
            colonnes = len(lignes[0])
            donnees = []
            
            for i, ligne in enumerate(lignes[1:], 1):  # Skip header
                if ligne:  # Ligne non vide
                    donnees.append(ligne)
            
            stats = {
                "nom_fichier": os.path.basename(fichier),
                "lignes_total": len(lignes),
                "lignes_donnees": len(donnees),
                "colonnes": colonnes,
                "en-tete": lignes[0] if lignes else [],
                "premiere_ligne": donnees[0] if donnees else [],
                "derniere_ligne": donnees[-1] if donnees else []
            }
            
            return stats
        except Exception as e:
            return {"erreur": str(e)}
    
    def analyser_json(self, fichier):
        """Analyse un fichier JSON"""
        try:
            with open(fichier, 'r') as f:
                data = json.load(f)
            
            stats = {
                "nom_fichier": os.path.basename(fichier),
                "type": type(data).__name__,
                "taille": len(str(data))
            }
            
            if isinstance(data, list):
                stats["elements"] = len(data)
                if data and isinstance(data[0], dict):
                    stats["cles"] = list(data[0].keys())[:5]  # 5 premières clés
            elif isinstance(data, dict):
                stats["cles"] = list(data.keys())[:5]
                stats["profondeur"] = self.calculer_profondeur(data)
            
            return stats
        except Exception as e:
            return {"erreur": str(e)}
    
    def calculer_profondeur(self, d, profondeur=0):
        """Calcule la profondeur d'un dictionnaire"""
        if not isinstance(d, dict) or not d:
            return profondeur
        
        profondeurs = []
        for valeur in d.values():
            if isinstance(valeur, dict):
                profondeurs.append(self.calculer_profondeur(valeur, profondeur + 1))
            else:
                profondeurs.append(profondeur + 1)
        
        return max(profondeurs) if profondeurs else profondeur + 1
    
    def creer_json_exemple(self):
        """Crée un fichier JSON d'exemple"""
        donnees = {
            "projet": "Agent IA",
            "version": "1.0",
            "modules": ["analyse", "ml", "web"],
            "statistiques": {
                "fichiers_crees": 25,
                "lignes_code": 1200,
                "derniere_maj": datetime.now().isoformat()
            },
            "auteurs": ["Utilisateur IA"]
        }
        
        with open('exemple_donnees.json', 'w') as f:
            json.dump(donnees, f, indent=2)
        
        return "exemple_donnees.json"
    
    def creer_csv_exemple(self):
        """Crée un fichier CSV d'exemple"""
        donnees = [
            ["Nom", "Age", "Ville", "Score"],
            ["Alice", "28", "Paris", "95"],
            ["Bob", "32", "Lyon", "88"],
            ["Charlie", "25", "Marseille", "92"],
            ["Diana", "30", "Toulouse", "85"]
        ]
        
        with open('exemple_donnees.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(donnees)
        
        return "exemple_donnees.csv"

def main():
    agent = AgentAnalyseDonnees()
    
    print("📊 AGENT D'ANALYSE DE DONNÉES")
    print("="*40)
    
    while True:
        print("\n1. Analyser un fichier CSV")
        print("2. Analyser un fichier JSON")
        print("3. Créer des fichiers d'exemple")
        print("4. Lister les fichiers de données")
        print("5. Quitter")
        
        choix = input("Choix : ")
        
        if choix == "1":
            fichier = input("Nom du fichier CSV : ")
            if os.path.exists(fichier):
                stats = agent.analyser_csv(fichier)
                if "erreur" in stats:
                    print(f"❌ Erreur : {stats['erreur']}")
                else:
                    print(f"\n📈 Statistiques CSV :")
                    for cle, valeur in stats.items():
                        if cle not in ["en-tete", "premiere_ligne", "derniere_ligne"]:
                            print(f"  • {cle} : {valeur}")
            else:
                print("❌ Fichier non trouvé")
        
        elif choix == "2":
            fichier = input("Nom du fichier JSON : ")
            if os.path.exists(fichier):
                stats = agent.analyser_json(fichier)
                if "erreur" in stats:
                    print(f"❌ Erreur : {stats['erreur']}")
                else:
                    print(f"\n📈 Statistiques JSON :")
                    for cle, valeur in stats.items():
                        print(f"  • {cle} : {valeur}")
            else:
                print("❌ Fichier non trouvé")
        
        elif choix == "3":
            print("\n📝 Création de fichiers d'exemple...")
            json_file = agent.creer_json_exemple()
            csv_file = agent.creer_csv_exemple()
            print(f"✅ {json_file} créé")
            print(f"✅ {csv_file} créé")
        
        elif choix == "4":
            print("\n📁 Fichiers de données :")
            fichiers = [f for f in os.listdir('.') if f.endswith(('.csv', '.json'))]
            if fichiers:
                for f in fichiers:
                    taille = os.path.getsize(f)
                    print(f"  • {f} ({taille} octets)")
            else:
                print("  Aucun fichier trouvé")
        
        elif choix == "5":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
EOF

python3 agent_analyse_donnees.py
