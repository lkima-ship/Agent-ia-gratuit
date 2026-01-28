# Effacer l'ancien fichier et créer une version correcte
cat > super_agent.py << 'EOF'
#!/usr/bin/env python3
"""
SUPER AGENT IA - Version simplifiée et fonctionnelle
"""

import os
import sys
import json
import sqlite3
import subprocess
import time
from datetime import datetime

class SuperAgent:
    def __init__(self, name="SuperAgent"):
        self.name = name
        self.version = "2.0"
        self.db_file = "agent_memory.db"
        self.setup_database()
        print(f"🤖 {self.name} v{self.version} - Prêt")
    
    def setup_database(self):
        """Initialise la base de données"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Table des actions
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    command TEXT,
                    result TEXT,
                    success INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            print(f"📁 Base de données '{self.db_file}' initialisée")
            return True
        except Exception as e:
            print(f"❌ Erreur base de données: {e}")
            return False
    
    def save_action(self, command, result, success=True):
        """Sauvegarde une action"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO actions (timestamp, command, result, success)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                command[:500],
                json.dumps(result)[:1000],
                1 if success else 0
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Erreur sauvegarde: {e}")
            return False
    
    def analyze_system(self):
        """Analyse simple du système"""
        print("\n" + "="*60)
        print("🔍 ANALYSE SYSTÈME")
        print("="*60)
        
        info = {
            "Système": os.uname().sysname,
            "Hôte": os.uname().nodename,
            "Répertoire": os.getcwd(),
            "Fichiers Python": len([f for f in os.listdir('.') if f.endswith('.py')]),
            "Heure": datetime.now().strftime("%H:%M:%S")
        }
        
        for key, value in info.items():
            print(f"  {key}: {value}")
        
        return info
    
    def execute_command(self, command):
        """Exécute une commande shell"""
        print(f"\n▶ Exécution: {command}")
        print("-"*50)
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
            print(f"Sortie:\n{result.stdout[:500]}")
            if result.stderr:
                print(f"Erreurs:\n{result.stderr[:500]}")
            
            # Sauvegarder l'action
            self.save_action(command, output, success=(result.returncode == 0))
            
            return output
        except subprocess.TimeoutExpired:
            print("❌ Timeout: Commande trop longue")
            return {"error": "timeout"}
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return {"error": str(e)}
    
    def quick_scan(self):
        """Scan rapide"""
        print("\n" + "="*60)
        print("⚡ SCAN RAPIDE")
        print("="*60)
        
        scans = [
            ("Fichiers Python", "find . -name '*.py' | head -10"),
            ("Processus", "ps aux | head -5"),
            ("Réseau", "ip addr 2>/dev/null | head -20 || ifconfig 2>/dev/null | head -20"),
            ("Disque", "df -h")
        ]
        
        for name, cmd in scans:
            print(f"\n📋 {name}:")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                print(result.stdout[:300])
            except:
                print("  (non disponible)")
    
    def show_history(self):
        """Affiche l'historique"""
        print("\n" + "="*60)
        print("📜 HISTORIQUE")
        print("="*60)
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute("SELECT timestamp, command FROM actions ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            
            if rows:
                for row in rows:
                    time_str = row[0][11:19]
                    cmd_preview = row[1][:50]
                    print(f"  {time_str} - {cmd_preview}...")
            else:
                print("  (aucun historique)")
            
            conn.close()
        except:
            print("  (erreur base de données)")
    
    def optimize_system(self):
        """Optimise le système"""
        print("\n" + "="*60)
        print("🧹 OPTIMISATION SYSTÈME")
        print("="*60)
        
        optimizations = []
        
        # 1. Nettoyage cache
        try:
            subprocess.run("rm -rf /tmp/* /var/tmp/* 2>/dev/null", shell=True)
            optimizations.append("✅ Cache nettoyé")
        except:
            optimizations.append("❌ Échec nettoyage cache")
        
        # 2. Vérification espace
        try:
            result = subprocess.run("df -h", shell=True, capture_output=True, text=True)
            optimizations.append("✅ Espace vérifié")
            print("\n💾 Espace disque:")
            print(result.stdout[:200])
        except:
            optimizations.append("❌ Échec vérification espace")
        
        # 3. Optimisation base
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute("VACUUM")
            conn.close()
            optimizations.append("✅ Base de données optimisée")
        except:
            optimizations.append("❌ Échec optimisation base")
        
        print("\n📊 RÉSULTATS:")
        for opt in optimizations:
            print(f"  {opt}")

def main_menu():
    """Menu principal"""
    agent = SuperAgent()
    
    while True:
        print("\n" + "="*60)
        print(f"🤖 SUPER AGENT v{agent.version}")
        print("="*60)
        print("1. 🔍 Analyser le système")
        print("2. ⚡ Scanner rapide")
        print("3. 💾 Exécuter une commande")
        print("4. 📜 Voir l'historique")
        print("5. 🧹 Optimiser le système")
        print("6. 🚪 Quitter")
        print("="*60)
        
        choix = input("\nVotre choix (1-6): ").strip()
        
        if choix == "1":
            agent.analyze_system()
        elif choix == "2":
            agent.quick_scan()
        elif choix == "3":
            cmd = input("Commande: ").strip()
            if cmd:
                agent.execute_command(cmd)
            else:
                print("❌ Commande vide")
        elif choix == "4":
            agent.show_history()
        elif choix == "5":
            agent.optimize_system()
        elif choix == "6":
            print("\n👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")
        
        if choix != "6":
            input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main_menu()
EOF
