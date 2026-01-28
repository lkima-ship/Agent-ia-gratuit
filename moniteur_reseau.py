#!/usr/bin/env python3
"""
MONITEUR RÉSEAU - Surveillance des connexions réseau
Version complète avec analyse en temps réel
"""

import os
import sys
import time
import subprocess
import platform
from datetime import datetime

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête du programme"""
    print("=" * 60)
    print("🌐 MONITEUR RÉSEAU")
    print("=" * 60)
    print()

def get_system_info():
    """Obtient les informations système"""
    system = platform.system()
    hostname = platform.node()
    return system, hostname

def check_network_interfaces():
    """Vérifie les interfaces réseau disponibles"""
    print("📡 INTERFACES RÉSEAU:")
    print("-" * 40)
    
    if platform.system() == "Windows":
        try:
            result = subprocess.run(['ipconfig', '/all'], 
                                  capture_output=True, text=True, encoding='utf-8')
            lines = result.stdout.split('\n')
            
            interfaces = []
            current_interface = None
            for line in lines:
                if 'adaptateur' in line.lower() or 'adapter' in line.lower():
                    if current_interface:
                        interfaces.append(current_interface)
                    current_interface = {'name': line.strip(': '), 'ips': []}
                elif 'adresse ipv4' in line.lower() or 'ipv4 address' in line.lower():
                    if current_interface:
                        ip = line.split(':')[-1].strip()
                        current_interface['ips'].append(ip)
            
            if current_interface:
                interfaces.append(current_interface)
            
            for i, interface in enumerate(interfaces, 1):
                name = interface['name']
                ips = ', '.join(interface['ips']) if interface['ips'] else 'Aucune IP'
                print(f"{i}. {name}")
                print(f"   📍 IP: {ips}")
                print()
                
        except Exception as e:
            print(f"❌ Erreur: {e}")
            
    else:  # Linux/Mac
        try:
            # Utiliser ip ou ifconfig
            try:
                result = subprocess.run(['ip', 'addr', 'show'], 
                                      capture_output=True, text=True)
                output = result.stdout
            except:
                result = subprocess.run(['ifconfig'], 
                                      capture_output=True, text=True)
                output = result.stdout
            
            lines = output.split('\n')
            interface = None
            
            for line in lines:
                if line and not line.startswith(' '):
                    if interface:
                        print(f"{interface_number}. {interface['name']}")
                        if interface['ips']:
                            print(f"   📍 IP: {', '.join(interface['ips'])}")
                        if interface['mac']:
                            print(f"   🔒 MAC: {interface['mac']}")
                        print()
                    
                    # Nouvelle interface
                    interface_name = line.split(':')[0]
                    interface = {'name': interface_name, 'ips': [], 'mac': ''}
                    interface_number = len([i for i in lines if i and not i.startswith(' ')]) - 1
                    
                elif 'inet ' in line:
                    parts = line.strip().split()
                    for part in parts:
                        if '.' in part and not part.startswith('inet6'):
                            ip = part.split('/')[0]
                            interface['ips'].append(ip)
                elif 'ether ' in line or 'lladdr ' in line:
                    parts = line.strip().split()
                    for part in parts:
                        if ':' in part and len(part) == 17:
                            interface['mac'] = part
            
            # Afficher la dernière interface
            if interface:
                print(f"{interface_number}. {interface['name']}")
                if interface['ips']:
                    print(f"   📍 IP: {', '.join(interface['ips'])}")
                if interface['mac']:
                    print(f"   🔒 MAC: {interface['mac']}")
                print()
                    
        except Exception as e:
            print(f"❌ Erreur: {e}")

def check_active_connections():
    """Vérifie les connexions actives"""
    print("🔗 CONNEXIONS ACTIVES:")
    print("-" * 40)
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, encoding='cp1252')
        else:
            result = subprocess.run(['netstat', '-tun'], 
                                  capture_output=True, text=True)
        
        lines = result.stdout.split('\n')
        connections = []
        
        for line in lines:
            if 'ESTABLISHED' in line or 'LISTEN' in line or 'SYN_SENT' in line:
                connections.append(line.strip())
        
        if connections:
            for i, conn in enumerate(connections[:10], 1):  # Limiter à 10 connexions
                print(f"{i}. {conn}")
            if len(connections) > 10:
                print(f"\n... et {len(connections) - 10} autres connexions")
        else:
            print("Aucune connexion active trouvée.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()

def check_open_ports():
    """Vérifie les ports ouverts"""
    print("🚪 PORTS OUVERTS:")
    print("-" * 40)
    
    common_ports = {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS",
        21: "FTP",
        25: "SMTP",
        53: "DNS",
        3306: "MySQL",
        5432: "PostgreSQL",
        27017: "MongoDB",
        8080: "HTTP Alt"
    }
    
    try:
        if platform.system() == "Windows":
            result = subprocess.run(['netstat', '-an'], 
                                  capture_output=True, text=True, encoding='cp1252')
        else:
            result = subprocess.run(['ss', '-tuln'], 
                                  capture_output=True, text=True)
        
        lines = result.stdout.split('\n')
        ports_found = []
        
        for line in lines:
            if 'LISTEN' in line or '0.0.0.0:' in line or '127.0.0.1:' in line:
                parts = line.split()
                for part in parts:
                    if ':' in part and '.' in part:
                        try:
                            port = int(part.split(':')[-1])
                            ports_found.append(port)
                        except:
                            pass
        
        if ports_found:
            print("Ports en écoute:")
            for port in sorted(set(ports_found))[:15]:  # Limiter à 15 ports
                service = common_ports.get(port, "Inconnu")
                print(f"  🔸 Port {port}: {service}")
        else:
            print("Aucun port ouvert détecté.")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()

def check_ping():
    """Test de ping vers des serveurs connus"""
    print("📶 TEST DE CONNECTIVITÉ:")
    print("-" * 40)
    
    servers = [
        ("Google DNS", "8.8.8.8"),
        ("Cloudflare", "1.1.1.1"),
        ("OpenDNS", "208.67.222.222"),
        ("Localhost", "127.0.0.1")
    ]
    
    for name, ip in servers:
        try:
            if platform.system() == "Windows":
                result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                      capture_output=True, text=True)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                      capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {name} ({ip}) - Connecté")
            else:
                print(f"❌ {name} ({ip}) - Hors ligne")
                
        except Exception as e:
            print(f"⚠️  {name} ({ip}) - Erreur: {e}")
    
    print()

def check_bandwidth():
    """Vérifie l'utilisation de la bande passante (simplifié)"""
    print("📊 UTILISATION RÉSEAU:")
    print("-" * 40)
    
    try:
        if platform.system() == "Linux":
            # Essayer d'utiliser iftop, nload, ou vnstat
            for cmd in ['iftop', 'nload', 'vnstat']:
                try:
                    result = subprocess.run(['which', cmd], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"ℹ️  Utilisez '{cmd}' pour des statistiques détaillées")
                        break
                except:
                    pass
        elif platform.system() == "Windows":
            print("ℹ️  Utilisez 'perfmon' pour des statistiques détaillées")
        else:
            print("ℹ️  Utilisez les outils système pour les statistiques réseau")
        
        print("\nPour une analyse en temps réel, utilisez:")
        print("  - Linux: iftop, nload, bmon")
        print("  - Windows: Resource Monitor")
        print("  - Mac: Activity Monitor > Network")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()

def run_diagnostics():
    """Exécute des diagnostics réseau"""
    print("🔍 DIAGNOSTICS RÉSEAU:")
    print("-" * 40)
    
    print("1. Vérification de la table de routage...")
    time.sleep(0.5)
    
    try:
        if platform.system() == "Windows":
            subprocess.run(['route', 'print'], shell=True)
        else:
            subprocess.run(['route', '-n'])
    except:
        print("❌ Impossible d'afficher la table de routage")
    
    print("\n2. Vérification du DNS...")
    time.sleep(0.5)
    
    try:
        if platform.system() == "Windows":
            subprocess.run(['nslookup', 'google.com'], shell=True)
        else:
            subprocess.run(['dig', 'google.com', '+short'])
    except:
        print("❌ Impossible de tester le DNS")
    
    print("\n✅ Diagnostics terminés")

def real_time_monitor():
    """Moniteur réseau en temps réel"""
    print("⏱️  MONITEUR TEMPS RÉEL")
    print("-" * 40)
    print("Appuyez sur Ctrl+C pour arrêter...")
    print()
    
    try:
        update_count = 0
        while True:
            clear_screen()
            print_header()
            print(f"🔄 Actualisation #{update_count + 1}")
            print()
            
            system, hostname = get_system_info()
            print(f"💻 Système: {system}")
            print(f"🏠 Hostname: {hostname}")
            print(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
            print()
            
            # Affichage des sections principales
            check_network_interfaces()
            check_active_connections()
            check_open_ports()
            check_ping()
            
            print(f"\n⏳ Prochaine actualisation dans 5 secondes...")
            print("Appuyez sur Ctrl+C pour revenir au menu")
            
            time.sleep(5)
            update_count += 1
            
    except KeyboardInterrupt:
        print("\n⏹️  Moniteur arrêté")
        time.sleep(2)

def main_menu():
    """Menu principal du moniteur réseau"""
    while True:
        clear_screen()
        print_header()
        
        system, hostname = get_system_info()
        print(f"💻 Système: {system}")
        print(f"🏠 Hostname: {hostname}")
        print(f"🕐 {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        print("📋 MENU PRINCIPAL:")
        print("1. 📡 Voir les interfaces réseau")
        print("2. 🔗 Voir les connexions actives")
        print("3. 🚪 Voir les ports ouverts")
        print("4. 📶 Tester la connectivité (ping)")
        print("5. 📊 Voir l'utilisation réseau")
        print("6. 🔍 Exécuter des diagnostics")
        print("7. ⏱️  Moniteur temps réel")
        print("8. 🧹 Effacer l'écran")
        print("9. ❌ Quitter le moniteur")
        print("\n" + "-" * 40)
        
        choice = input("\nVotre choix (1-9): ").strip()
        
        if choice == "1":
            clear_screen()
            print_header()
            check_network_interfaces()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "2":
            clear_screen()
            print_header()
            check_active_connections()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "3":
            clear_screen()
            print_header()
            check_open_ports()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "4":
            clear_screen()
            print_header()
            check_ping()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "5":
            clear_screen()
            print_header()
            check_bandwidth()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "6":
            clear_screen()
            print_header()
            run_diagnostics()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "7":
            real_time_monitor()
        elif choice == "8":
            clear_screen()
        elif choice == "9":
            print("\n👋 Au revoir !")
            time.sleep(1)
            break
        else:
            print("\n❌ Choix invalide !")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⏹️  Moniteur réseau interrompu.")
        time.sleep(1)
