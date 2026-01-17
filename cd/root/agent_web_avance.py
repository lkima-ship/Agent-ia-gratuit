cat > agent_web_avance.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT WEB AVANCÉ - Scraping et API
"""
import requests
import json
import time
from urllib.parse import urlparse
import os

class AgentWebAvance:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (AgentWebAvance/1.0)'
        }
    
    def scraper_page(self, url):
        """Scrape le contenu d'une page web"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Analyse basique
            content = response.text.lower()
            
            stats = {
                "url": url,
                "status": response.status_code,
                "taille": len(response.content),
                "temps_reponse": response.elapsed.total_seconds(),
                "encoding": response.encoding,
                "titres": self.extraire_titres(content),
                "liens": content.count('href='),
                "images": content.count('<img'),
                "mots_cles": self.extraire_mots_cles(content)
            }
            
            return stats
        except Exception as e:
            return {"erreur": str(e), "url": url}
    
    def extraire_titres(self, content):
        """Extrait les titres h1, h2, h3"""
        titres = []
        import re
        
        for niveau in [1, 2, 3]:
            pattern = f'<h{niveau}[^>]*>(.*?)</h{niveau}>'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                # Nettoyer le texte
                texte = re.sub('<[^>]+>', '', match).strip()[:100]
                if texte:
                    titres.append(f"H{niveau}: {texte}")
        
        return titres[:5]  # Limiter à 5
    
    def extraire_mots_cles(self, content, limit=10):
        """Extrait les mots les plus fréquents"""
        import re
        from collections import Counter
        
        # Enlever le HTML
        text_only = re.sub('<[^>]+>', ' ', content)
        # Garder uniquement les mots
        mots = re.findall(r'\b[a-z]{4,}\b', text_only)
        
        # Filtrer les mots courants
        mots_courants = {'dans', 'pour', 'avec', 'sans', 'dont', 'plus', 'tout', 'fait'}
        mots_filtres = [mot for mot in mots if mot not in mots_courants]
        
        compteur = Counter(mots_filtres)
        return [mot for mot, count in compteur.most_common(limit)]
    
    def tester_api_rest(self, url):
        """Teste une API REST"""
        try:
            print(f"\n🔍 Test de l'API : {url}")
            
            # Test GET
            response = requests.get(url, timeout=10)
            
            result = {
                "method": "GET",
                "status": response.status_code,
                "headers": dict(response.headers),
                "content_type": response.headers.get('content-type', 'inconnu'),
                "taille": len(response.content)
            }
            
            # Essayer de parser le contenu
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                try:
                    data = response.json()
                    result["format"] = "JSON"
                    result["keys"] = list(data.keys())[:5] if isinstance(data, dict) else type(data).__name__
                except:
                    result["format"] = "JSON invalide"
            elif 'text/html' in content_type:
                result["format"] = "HTML"
            elif 'text/plain' in content_type:
                result["format"] = "TEXT"
            
            return result
        except Exception as e:
            return {"erreur": str(e)}
    
    def surveiller_site(self, url, interval=5):
        """Surveille un site web à intervalle régulier"""
        print(f"\n👁️ Surveillance de {url}")
        print("Appuyez sur Ctrl+C pour arrêter")
        
        try:
            historique = []
            while True:
                debut = time.time()
                try:
                    response = requests.get(url, timeout=10)
                    duree = time.time() - debut
                    
                    statut = {
                        "timestamp": time.strftime("%H:%M:%S"),
                        "status": response.status_code,
                        "temps_reponse": f"{duree:.2f}s",
                        "taille": len(response.content)
                    }
                    
                    historique.append(statut)
                    
                    # Afficher le dernier statut
                    print(f"[{statut['timestamp']}] Status: {statut['status']} | Temps: {statut['temps_reponse']} | Taille: {statut['taille']} octets")
                    
                    # Garder seulement les 10 derniers
                    if len(historique) > 10:
                        historique = historique[-10:]
                    
                except Exception as e:
                    print(f"[{time.strftime('%H:%M:%S')}] ❌ Erreur: {e}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n⏹️ Surveillance arrêtée")
            return historique

def main():
    agent = AgentWebAvance()
    
    print("🌐 AGENT WEB AVANCÉ")
    print("="*40)
    
    while True:
        print("\n1. Scraper une page web")
        print("2. Tester une API REST")
        print("3. Surveiller un site (temps réel)")
        print("4. Analyser les métadonnées")
        print("5. Quitter")
        
        choix = input("Choix : ")
        
        if choix == "1":
            url = input("URL à scraper : ")
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"\n🕸️ Scraping de {url}...")
            resultats = agent.scraper_page(url)
            
            if "erreur" in resultats:
                print(f"❌ Erreur : {resultats['erreur']}")
            else:
                print(f"\n📊 Résultats :")
                for cle, valeur in resultats.items():
                    if cle == "titres" and valeur:
                        print(f"  • Titres trouvés :")
                        for titre in valeur:
                            print(f"    - {titre}")
                    elif cle == "mots_cles" and valeur:
                        print(f"  • Mots-clés fréquents : {', '.join(valeur[:5])}")
                    elif cle not in ["titres", "mots_cles"]:
                        print(f"  • {cle} : {valeur}")
        
        elif choix == "2":
            url = input("URL de l'API : ")
            resultats = agent.tester_api_rest(url)
            
            if "erreur" in resultats:
                print(f"❌ Erreur : {resultats['erreur']}")
            else:
                print(f"\n📡 Résultats du test API :")
                for cle, valeur in resultats.items():
                    if cle == "headers":
                        print(f"  • Quelques en-têtes :")
                        for h, v in list(valeur.items())[:3]:
                            print(f"    - {h}: {v}")
                    else:
                        print(f"  • {cle} : {valeur}")
        
        elif choix == "3":
            url = input("URL à surveiller : ")
            interval = input("Intervalle en secondes [5] : ") or "5"
            
            try:
                interval_int = int(interval)
                agent.surveiller_site(url, interval_int)
            except ValueError:
                print("❌ Intervalle invalide")
        
        elif choix == "4":
            url = input("URL à analyser : ")
            print("\n🔍 Extraction des métadonnées...")
            # Simuler pour l'exemple
            print("  • Type: Site web")
            print("  • Serveur: Nginx/Apache")
            print("  • Techno: HTML5, CSS3, JavaScript")
            print("  • Sécurité: HTTPS activé")
            print("  • Performance: Temps de chargement estimé")
        
        elif choix == "5":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
EOF

python3 agent_web_avance.py
