cat > super_agent.py << 'EOF'
#!/usr/bin/env python3
"""
SUPER AGENT IA - Version Alpine Compatible
"""

import os
import sys
import json
import sqlite3
from datetime import datetime
import subprocess
import hashlib
import time

class SuperAgent:
    """Agent IA intelligent et rapide pour Alpine"""
    
    def __init__(self, name="SuperAgent"):
        self.name = name
        self.version = "3.0.0"
        self.db_file = "agent_memory.db"
        self.setup_database()
        
    def setup_database(self):
        """Crée la base de données SQLite"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Table des mémoires
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                result TEXT,
                success INTEGER
            )
        ''')
        
        # Table des connaissances
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern TEXT UNIQUE,
                solution TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        # Table des performances
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_name TEXT,
                execution_time REAL,
                timestamp TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"✅ Base de données '{self.db_file}' initialisée")
    
    def analyze_system(self):
        """Analyse rapide du système Alpine"""
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "hostname": os.uname().nodename,
            "system": os.uname().sysname,
            "release": os.uname().release,
            "python_version": sys.version,
            "current_dir": os.getcwd(),
            "files_count": len(os.listdir('.')),
            "disk_usage": self.get_disk_usage(),
            "memory_info": self.get_memory_info(),
            "cpu_info": self.get_cpu_info()
        }
        
        return analysis
    
    def get_disk_usage(self):
        """Récupère l'utilisation du disque"""
        try:
            stat = os.statvfs('/')
            total = stat.f_blocks * stat.f_frsize
            used = (stat.f_blocks - stat.f_bfree) * stat.f_frsize
            percent = (used / total) * 100
            return f"{percent:.1f}%"
        except:
            return "N/A"
    
    def get_memory_info(self):
        """Récupère les informations mémoire"""
        try:
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                meminfo = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        meminfo[key.strip()] = value.strip()
                
                total = int(meminfo.get('MemTotal', '0 kB').split()[0])
                free = int(meminfo.get('MemFree', '0 kB').split()[0])
                cached = int(meminfo.get('Cached', '0 kB').split()[0])
                
                used = total - free - cached
                percent = (used / total) * 100 if total > 0 else 0
                return f"{percent:.1f}%"
        except:
            return "N/A"
    
    def get_cpu_info(self):
        """Récupère les informations CPU"""
        try:
            with open('/proc/cpuinfo', 'r') as f:
                content = f.read()
                processors = content.count('processor')
                return f"{processors} core(s)"
        except:
            return "N/A"
    
    def optimize_system(self):
        """Optimisations pour Alpine Linux"""
        optimizations = []
        
        # 1. Nettoyage du cache APK
        try:
            subprocess.run(['apk', 'cache', 'clean'], capture_output=True)
            optimizations.append("Cache APK nettoyé")
        except:
            pass
        
        # 2. Suppression des fichiers temporaires
        temp_dirs = ['/tmp', '/var/tmp']
        for temp_dir in temp_dirs:
            if os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                os.unlink(item_path)
                            optimizations.append(f"Fichiers temporaires supprimés de {temp_dir}")
                        except:
                            continue
                except:
                    pass
        
        # 3. Optimisation des bases de données SQLite
        try:
            conn = sqlite3.connect(self.db_file)
            conn.execute("VACUUM")
            conn.close()
            optimizations.append("Base de données optimisée (VACUUM)")
        except:
            pass
        
        return optimizations
    
    def learn_command(self, command, result, success=True):
        """Apprend d'une commande exécutée"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Hash de la commande comme pattern
        pattern_hash = hashlib.md5(command.encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT OR REPLACE INTO knowledge 
            (pattern, solution, success_count, failure_count, last_used)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            pattern_hash,
            json.dumps({"command": command, "result": result}),
            1 if success else 0,
            0 if success else 1,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        status = "succès" if success else "échec"
        print(f"📚 Apprentissage: {command[:50]}... ({status})")
    
    def suggest_command(self, partial_command):
        """Suggère une commande complète basée sur l'historique"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT solution 
            FROM knowledge 
            WHERE solution LIKE ? 
            ORDER BY success_count DESC 
            LIMIT 1
        ''', (f'%{partial_command}%',))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            data = json.loads(result[0])
            return data.get("command", "")
        
        return None
    
    def quick_scan(self):
        """Scan rapide du système"""
        print("\n" + "="*60)
        print("🔍 SCAN RAPIDE DU SYSTÈME")
        print("="*60)
        
        checks = [
            ("Fichiers Python", lambda: len([f for f in os.listdir('.') if f.endswith('.py')])),
            ("Fichiers exécutables", lambda: len([f for f in os.listdir('.') if os.access(f, os.X_OK)])),
            ("Base de connaissances", lambda: self.get_knowledge_count()),
            ("Dernière optimisation", lambda: self.get_last_optimization()),
            ("Espace disque", self.get_disk_usage),
            ("Utilisation mémoire", self.get_memory_info)
        ]
        
        for check_name, check_func in checks:
            try:
                result = check_func()
                print(f"  {check_name:25}: {result}")
            except Exception as e:
                print(f"  {check_name:25}: Erreur - {e}")
        
        print("="*60)
    
    def get_knowledge_count(self):
        """Compte les entrées dans la base de connaissances"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM knowledge")
        count = cursor.fetchone()[0]
        conn.close()
        return f"{count} entrées"
    
    def get_last_optimization(self):
        """Récupère la dernière optimisation"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        cursor.execute("SELECT timestamp FROM memories WHERE action='optimization' ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return f"le {result[0][:10]}"
        return "Jamais"
    
    def save_memory(self, action, result, success=True):
        """Sauvegarde une action en mémoire"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO memories (timestamp, action, result, success)
            VALUES (?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            action,
            json.dumps(result),
            1 if success else 0
        ))
        
        conn.commit()
        conn.close()

def main_menu():
    """Menu principal de l'agent"""
    agent = SuperAgent()
    
    while True:
        print("\n" + "="*60)
        print(f"🤖 SUPER AGENT IA - v{agent.version}")
        print("="*60)
        print("1. 🔍 Analyser le système")
        print("2. ⚡ Scanner rapide")
        print("3. 🧹 Optimiser le système")
        print("4. 💾 Exécuter une commande")
        print("5. 📚 Voir l'historique")
        print("6. 🎓 Mode apprentissage")
        print("7. 🚀 Quitter")
        print("="*60)
        
        choix = input("\nVotre choix (1-7): ").strip()
        
        if choix == "1":
            print("\nAnalyse en cours...")
            analysis = agent.analyze_system()
            print(json.dumps(analysis, indent=2))
            agent.save_memory("system_analysis", analysis)
            
        elif choix == "2":
            agent.quick_scan()
            agent.save_memory("quick_scan", {"action": "scan"})
            
        elif choix == "3":
            print("\nOptimisation en cours...")
            optimizations = agent.optimize_system()
            print("✅ Optimisations appliquées:")
            for opt in optimizations:
                print(f"  - {opt}")
            agent.save_memory("optimization", optimizations)
            
        elif choix == "4":
            command = input("Commande à exécuter: ").strip()
            if command:
                print(f"\nExécution: {command}")
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(f"Sortie:\n{result.stdout}")
                    if result.stderr:
                        print(f"Erreurs:\n{result.stderr}")
                    
                    # Apprendre de cette commande
                    agent.learn_command(
                        command, 
                        {"stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode},
                        success=(result.returncode == 0)
                    )
                except Exception as e:
                    print(f"❌ Erreur: {e}")
                    agent.learn_command(command, {"error": str(e)}, success=False)
            else:
                print("❌ Commande vide!")
                
        elif choix == "5":
            print("\n📜 HISTORIQUE RÉCENT:")
            conn = sqlite3.connect(agent.db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, action FROM memories ORDER BY id DESC LIMIT 10")
            for row in cursor.fetchall():
                print(f"  {row[0][:19]} - {row[1]}")
            conn.close()
            
        elif choix == "6":
            print("\n🎓 MODE APPRENTISSAGE")
            pattern = input("Description du problème: ").strip()
            solution = input("Solution/Commande: ").strip()
            success = input("Succès? (oui/non): ").strip().lower() == "oui"
            
            agent.learn_command(solution, {"pattern": pattern}, success)
            print("✅ Apprentissage enregistré!")
            
        elif choix == "7":
            print("\n👋 Au revoir! L'agent reste en veille.")
            break
            
        else:
            print("❌ Choix invalide!")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main_menu()
EOF
