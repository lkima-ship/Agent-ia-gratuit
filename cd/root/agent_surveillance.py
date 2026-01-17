cat > agent_surveillance.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT DE SURVEILLANCE SYSTÈME
"""
import os
import time
import psutil
import json
from datetime import datetime
import socket

class AgentSurveillance:
    def __init__(self):
        self.log_file = "surveillance_log.json"
        self.charger_logs()
    
    def charger_logs(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return []
    
    def sauvegarder_log(self, donnees):
        logs = self.charger_logs()
        logs.append(donnees)
        
        # Garder seulement les 100 derniers logs
        if len(logs) > 100:
            logs = logs[-100:]
        
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def obtenir_stats_systeme(self):
        """Obtenir les statistiques système"""
        stats = {
            "timestamp": datetime.now().isoformat(),
            "cpu": {
                "pourcentage": psutil.cpu_percent(interval=1),
                "count": psutil.cpu_count(),
                "freq": psutil.cpu_freq().current if hasattr(psutil.cpu_freq(), 'current') else "N/A"
            },
            "memoire": {
                "total": psutil.virtual_memory().total,
                "disponible": psutil.virtual_memory().available,
                "pourcentage": psutil.virtual_memory().percent,
                "utilise": psutil.virtual_memory().used
            },
            "disque": {
                "total": psutil.disk_usage('/').total,
                "utilise": psutil.disk_usage('/').used,
                "libre": psutil.disk_usage('/').free,
                "pourcentage": psutil.disk_usage('/').percent
            },
            "reseau": {
                "connexions": len(psutil.net_connections()),
                "adresses": self.obtenir_adresses_ip()
            },
            "processus": {
                "total": len(psutil.pids()),
                "python": self.compter_processus_python()
            }
        }
        
        # Convertir les octets en Go pour lisibilité
        stats["memoire"]["total_gb"] = round(stats["memoire"]["total"] / (1024**3), 2)
        stats["memoire"]["utilise_gb"] = round(stats["memoire"]["utilise"] / (1024**3), 2)
        stats["disque"]["total_gb"] = round(stats["disque"]["total"] / (1024**3), 2)
        stats["disque"]["utilise_gb"] = round(stats["disque"]["utilise"] / (1024**3), 2)
        
        return stats
    
    def obtenir_adresses_ip(self):
        """Obtenir les adresses IP"""
        adresses = []
        try:
            hostname = socket.gethostname()
            adresses.append(f"Hostname: {hostname}")
            
            # IP locale
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_locale = s.getsockname()[0]
            s.close()
            adresses.append(f"Locale: {ip_locale}")
        except:
            adresses.append("IP: Indisponible")
        
        return adresses
    
    def compter_processus_python(self):
        """Compter les processus Python"""
        count = 0
        for proc in psutil.process_iter(['name']):
            try:
                if 'python' in proc.info['name'].lower():
                    count += 1
            except:
                pass
        return count
    
    def surveiller_en_temps_reel(self, interval=2):
        """Surveillance en temps réel"""
        print(f"\n👁️ Surveillance système démarrée (intervalle: {interval}s)")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("-"*50)
        
        try:
            while True:
                stats = self.obtenir_stats_systeme()
                
                # Affichage formaté
                print(f"\n🕐 {datetime.now().strftime('%H:%M:%S')}")
                print(f"💻 CPU: {stats['cpu']['pourcentage']}% | Cœurs: {stats['cpu']['count']}")
                print(f"🧠 Mémoire: {stats['memoire']['pourcentage']}% ({stats['memoire']['utilise_gb']}/{stats['memoire']['total_gb']} GB)")
                print(f"💾 Disque: {stats['disque']['pourcentage']}% utilisés")
                print(f"📡 Processus: {stats['processus']['total']} total, {stats['processus']['python']} Python")
                
                # Sauvegarder
                self.sauvegarder_log(stats)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️ Surveillance arrêtée")
    
    def generer_rapport(self):
        """Génère un rapport détaillé"""
        logs = self.charger_logs()
        
        if not logs:
            return {"erreur": "Aucun log disponible"}
        
        # Analyse des logs
        cpu_values = [log['cpu']['pourcentage'] for log in logs]
        mem_values = [log['memoire']['pourcentage'] for log in logs]
        
        rapport = {
            "periode": f"{len(logs)} échantillons",
            "cpu": {
                "moyenne": round(sum(cpu_values) / len(cpu_values), 1),
                "max": round(max(cpu_values), 1),
                "min": round(min(cpu_values), 1)
            },
            "memoire": {
                "moyenne": round(sum(mem_values) / len(mem_values), 1),
                "max": round(max(mem_values), 1),
                "min": round(min(mem_values), 1)
            },
            "dernier_log": logs[-1] if logs else None
        }
        
        return rapport

def main():
    try:
        import psutil
    except ImportError:
        print("❌ psutil non installé. Installation...")
        os.system("python3 -m pip install psutil --quiet")
        import psutil
    
    agent = AgentSurveillance()
    
    print("🔧 AGENT DE SURVEILLANCE SYSTÈME")
    print("="*40)
    
    while True:
        print("\n1. Voir état actuel")
        print("2. Surveillance temps réel")
        print("3. Générer rapport")
        print("4. Voir les logs")
        print("5. Quitter")
        
        choix = input("Choix : ")
        
        if choix == "1":
            stats = agent.obtenir_stats_systeme()
            print(f"\n📊 ÉTAT SYSTÈME ACTUEL :")
            print(f"🕐 Heure : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"\n💻 CPU :")
            print(f"  • Utilisation : {stats['cpu']['pourcentage']}%")
            print(f"  • Cœurs : {stats['cpu']['count']}")
            print(f"  • Fréquence : {stats['cpu']['freq']} MHz")
            
            print(f"\n🧠 MÉMOIRE :")
            print(f"  • Utilisation : {stats['memoire']['pourcentage']}%")
            print(f"  • Total : {stats['memoire']['total_gb']} GB")
            print(f"  • Utilisé : {stats['memoire']['utilise_gb']} GB")
            
            print(f"\n💾 DISQUE :")
            print(f"  • Utilisation : {stats['disque']['pourcentage']}%")
            print(f"  • Total : {stats['disque']['total_gb']} GB")
            print(f"  • Utilisé : {stats['disque']['utilise_gb']} GB")
            
            print(f"\n📡 RÉSEAU & PROCESSUS :")
            print(f"  • Processus totaux : {stats['processus']['total']}")
            print(f"  • Processus Python : {stats['processus']['python']}")
            for addr in stats['reseau']['adresses']:
                print(f"  • {addr}")
        
        elif choix == "2":
            interval = input("Intervalle en secondes [2] : ") or "2"
            try:
                interval_int = int(interval)
                agent.surveiller_en_temps_reel(interval_int)
            except ValueError:
                print("❌ Intervalle invalide")
        
        elif choix == "3":
            rapport = agent.generer_rapport()
            if "erreur" in rapport:
                print(f"❌ {rapport['erreur']}")
            else:
                print(f"\n📄 RAPPORT DE SURVEILLANCE :")
                print(f"📅 Période : {rapport['periode']}")
                print(f"\n📈 CPU :")
                print(f"  • Moyenne : {rapport['cpu']['moyenne']}%")
                print(f"  • Max : {rapport['cpu']['max']}%")
                print(f"  • Min : {rapport['cpu']['min']}%")
                print(f"\n📊 MÉMOIRE :")
                print(f"  • Moyenne : {rapport['memoire']['moyenne']}%")
                print(f"  • Max : {rapport['memoire']['max']}%")
                print(f"  • Min : {rapport['memoire']['min']}%")
        
        elif choix == "4":
            logs = agent.charger_logs()
            print(f"\n📁 LOGS ({len(logs)} entrées) :")
            for i, log in enumerate(logs[-5:], 1):  # 5 derniers
                heure = datetime.fromisoformat(log['timestamp']).strftime('%H:%M')
                print(f"{i}. [{heure}] CPU: {log['cpu']['pourcentage']}% | Mémoire: {log['memoire']['pourcentage']}%")
        
        elif choix == "5":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
EOF

python3 agent_surveillance.py
