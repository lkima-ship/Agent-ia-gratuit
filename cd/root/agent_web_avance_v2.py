cd /root

# Créer la version améliorée de l'agent web
cat > agent_web_avance_v2.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT WEB AVANCÉ V2 - Scraping réel, API, Surveillance
"""
import requests
import json
import time
import os
import sys
import socket
from datetime import datetime
from urllib.parse import urlparse, urljoin, quote_plus
from bs4 import BeautifulSoup
import csv

class AgentWebAvanceV2:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        })
        self.historique = []
        self.log_file = "web_agent_log.json"
        self.charger_historique()
    
    def charger_historique(self):
        """Charge l'historique des analyses"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    self.historique = json.load(f)
            except:
                self.historique = []
    
    def sauvegarder_historique(self):
        """Sauvegarde l'historique"""
        with open(self.log_file, 'w') as f:
            json.dump(self.historique[-100:], f, indent=2)
    
    def verifier_connexion(self):
        """Vérifie la connexion internet"""
        tests = [
            ("Google", "https://www.google.com"),
            ("Cloudflare", "https://1.1.1.1"),
            ("OpenDNS", "https://www.opendns.com")
        ]
        
        resultats = []
        for nom, url in tests:
            try:
                start = time.time()
                response = self.session.get(url, timeout=5)
                duree = time.time() - start
                resultats.append({
                    "service": nom,
                    "statut": "✅" if response.status_code == 200 else "❌",
                    "temps": f"{duree:.2f}s",
                    "code": response.status_code
                })
            except Exception as e:
                resultats.append({
                    "service": nom,
                    "statut": "❌",
                    "temps": "N/A",
                    "erreur": str(e)
                })
        
        return resultats
    
    def scraper_url(self, url, profondeur=1):
        """Scrape une URL avec une profondeur donnée"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            print(f"\n🔍 Scraping de {url} (profondeur: {profondeur})...")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extraire les informations
            donnees = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "encoding": response.encoding,
                "headers": dict(response.headers),
                "content_type": response.headers.get('content-type', ''),
                "taille": len(response.content),
                "temps_reponse": response.elapsed.total_seconds(),
                "titre": self.extraire_titre(soup),
                "meta_description": self.extraire_meta_description(soup),
                "meta_keywords": self.extraire_meta_keywords(soup),
                "langue": self.extraire_langue(soup),
                "liens": self.extraire_liens(soup, url),
                "images": self.extraire_images(soup, url),
                "textes": self.extraire_textes_importants(soup),
                "structure": self.analyser_structure(soup)
            }
            
            # Suivre les liens si profondeur > 1
            if profondeur > 1:
                donnees["liens_profond"] = []
                liens_uniques = list(set(donnees["liens"]["internes"][:5]))  # 5 premiers liens internes
                
                for lien in liens_uniques:
                    try:
                        sous_donnees = self.scraper_url(lien, profondeur-1)
                        donnees["liens_profond"].append(sous_donnees)
                    except:
                        continue
            
            # Sauvegarder dans l'historique
            self.historique.append({
                "type": "scraping",
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "donnees": donnees
            })
            self.sauvegarder_historique()
            
            return donnees
            
        except Exception as e:
            return {"erreur": str(e), "url": url}
    
    def extraire_titre(self, soup):
        """Extrait le titre de la page"""
        if soup.title:
            return soup.title.string.strip()
        return "Pas de titre"
    
    def extraire_meta_description(self, soup):
        """Extrait la meta description"""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            return meta['content'].strip()[:200]
        return "Pas de description"
    
    def extraire_meta_keywords(self, soup):
        """Extrait les meta keywords"""
        meta = soup.find('meta', attrs={'name': 'keywords'})
        if meta and meta.get('content'):
            return meta['content'].strip()[:200]
        return "Pas de keywords"
    
    def extraire_langue(self, soup):
        """Extrait la langue de la page"""
        html = soup.find('html')
        if html and html.get('lang'):
            return html['lang']
        return "Non détecté"
    
    def extraire_liens(self, soup, url_base):
        """Extrait tous les liens de la page"""
        liens = soup.find_all('a', href=True)
        
        internes = []
        externes = []
        
        for lien in liens:
            href = lien['href'].strip()
            if href:
                # Normaliser l'URL
                try:
                    full_url = urljoin(url_base, href)
                    if urlparse(full_url).netloc == urlparse(url_base).netloc:
                        internes.append(full_url)
                    else:
                        externes.append(full_url)
                except:
                    continue
        
        return {
            "total": len(liens),
            "internes": list(set(internes))[:20],  # Limiter à 20
            "externes": list(set(externes))[:20]
        }
    
    def extraire_images(self, soup, url_base):
        """Extrait toutes les images de la page"""
        images = soup.find_all('img', src=True)
        
        donnees_images = []
        for img in images[:10]:  # Limiter à 10 images
            src = img.get('src', '').strip()
            alt = img.get('alt', '').strip()[:100]
            
            if src:
                try:
                    full_src = urljoin(url_base, src)
                    donnees_images.append({
                        "src": full_src,
                        "alt": alt if alt else "Pas d'alt",
                        "title": img.get('title', '')
                    })
                except:
                    continue
        
        return {
            "total": len(images),
            "images": donnees_images
        }
    
    def extraire_textes_importants(self, soup):
        """Extrait les textes importants (h1, h2, h3, p)"""
        textes = {
            "h1": [],
            "h2": [],
            "h3": [],
            "paragraphes": []
        }
        
        # Extraire les titres
        for niveau in ['h1', 'h2', 'h3']:
            for tag in soup.find_all(niveau):
                texte = tag.get_text().strip()
                if texte:
                    textes[niveau].append(texte[:200])
        
        # Extraire quelques paragraphes
        for p in soup.find_all('p')[:10]:
            texte = p.get_text().strip()
            if texte and len(texte) > 20:
                textes["paragraphes"].append(texte[:200])
        
        # Compter les mots
        tous_textes = ' '.join(textes["h1"] + textes["h2"] + textes["h3"] + textes["paragraphes"])
        mots = len(tous_textes.split())
        
        textes["statistiques"] = {
            "mots_total": mots,
            "h1_count": len(textes["h1"]),
            "h2_count": len(textes["h2"]),
            "h3_count": len(textes["h3"]),
            "paragraphes_count": len(textes["paragraphes"])
        }
        
        return textes
    
    def analyser_structure(self, soup):
        """Analyse la structure HTML de la page"""
        elements = {
            "div": len(soup.find_all('div')),
            "span": len(soup.find_all('span')),
            "table": len(soup.find_all('table')),
            "form": len(soup.find_all('form')),
            "input": len(soup.find_all('input')),
            "button": len(soup.find_all('button')),
            "script": len(soup.find_all('script')),
            "style": len(soup.find_all('style')),
            "link": len(soup.find_all('link')),
            "meta": len(soup.find_all('meta'))
        }
        
        # Détecter les frameworks
        frameworks = []
        html_str = str(soup)
        
        framework_indicators = {
            "React": ["react", "react-dom"],
            "Vue.js": ["vue", "v-app"],
            "Angular": ["ng-", "angular"],
            "jQuery": ["jquery", "$("],
            "Bootstrap": ["bootstrap", "btn btn-"],
            "Tailwind": ["tailwind", "class=.*tw-"],
            "WordPress": ["wp-", "wordpress"],
            "Joomla": ["joomla"],
            "Drupal": ["drupal"]
        }
        
        for framework, indicators in framework_indicators.items():
            for indicator in indicators:
                if indicator in html_str.lower():
                    frameworks.append(framework)
                    break
        
        return {
            "elements": elements,
            "frameworks": list(set(frameworks)),
            "doctype": self.extraire_doctype(soup)
        }
    
    def extraire_doctype(self, soup):
        """Extrait le doctype"""
        for item in soup.contents:
            if isinstance(item, str) and item.strip().startswith('<!DOCTYPE'):
                return item.strip()
        return "HTML5 (par défaut)"
    
    def tester_api(self, url, method="GET", data=None, headers=None):
        """Teste une API REST"""
        try:
            if not headers:
                headers = {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            
            start = time.time()
            
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=10)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=10)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=10)
            else:
                return {"erreur": f"Méthode {method} non supportée"}
            
            duree = time.time() - start
            
            resultat = {
                "url": url,
                "method": method,
                "status_code": response.status_code,
                "temps_reponse": f"{duree:.2f}s",
                "headers": dict(response.headers),
                "content_type": response.headers.get('content-type', ''),
                "taille": len(response.content)
            }
            
            # Essayer de parser la réponse
            try:
                if 'application/json' in response.headers.get('content-type', ''):
                    resultat["body"] = response.json()
                else:
                    resultat["body_preview"] = response.text[:500]
            except:
                resultat["body_raw"] = response.text[:500]
            
            # Sauvegarder
            self.historique.append({
                "type": "api_test",
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "resultat": resultat
            })
            self.sauvegarder_historique()
            
            return resultat
            
        except Exception as e:
            return {"erreur": str(e), "url": url}
    
    def surveiller_site(self, url, interval=30, duree=300):
        """Surveille un site pendant une durée donnée"""
        print(f"\n👁️ Surveillance de {url}")
        print(f"⏱️  Intervalle: {interval}s, Durée: {duree}s")
        print("Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        stats = {
            "url": url,
            "debut": datetime.now().isoformat(),
            "tests": [],
            "statistiques": {}
        }
        
        start_time = time.time()
        test_count = 0
        
        try:
            while time.time() - start_time < duree:
                test_count += 1
                print(f"\nTest #{test_count} - {datetime.now().strftime('%H:%M:%S')}")
                
                try:
                    test_start = time.time()
                    response = self.session.get(url, timeout=10)
                    test_duree = time.time() - test_start
                    
                    statut = {
                        "timestamp": datetime.now().isoformat(),
                        "status": response.status_code,
                        "temps": f"{test_duree:.2f}s",
                        "taille": len(response.content),
                        "succes": response.status_code == 200
                    }
                    
                    stats["tests"].append(statut)
                    
                    # Afficher
                    statut_symbole = "✅" if statut["succes"] else "❌"
                    print(f"{statut_symbole} Status: {statut['status']} | Temps: {statut['temps']}")
                    
                except Exception as e:
                    erreur_statut = {
                        "timestamp": datetime.now().isoformat(),
                        "erreur": str(e),
                        "succes": False
                    }
                    stats["tests"].append(erreur_statut)
                    print(f"❌ Erreur: {e}")
                
                # Attendre l'intervalle (sauf au dernier tour)
                if time.time() - start_time + interval < duree:
                    time.sleep(interval)
                else:
                    break
        
        except KeyboardInterrupt:
            print("\n⏹️ Surveillance interrompue")
        
        # Calculer les statistiques
        if stats["tests"]:
            succes = [t for t in stats["tests"] if t.get("succes", False)]
            stats["statistiques"] = {
                "total_tests": len(stats["tests"]),
                "tests_succes": len(succes),
                "taux_succes": f"{(len(succes)/len(stats['tests'])*100):.1f}%" if stats["tests"] else "0%",
                "fin": datetime.now().isoformat(),
                "duree_totale": f"{time.time() - start_time:.1f}s"
            }
        
        # Sauvegarder
        self.historique.append({
            "type": "surveillance",
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "stats": stats
        })
        self.sauvegarder_historique()
        
        return stats
    
    def analyser_seo(self, url):
        """Analyse SEO basique d'une URL"""
        try:
            donnees = self.scraper_url(url, profondeur=1)
            
            if "erreur" in donnees:
                return donnees
            
            score = 0
            recommendations = []
            
            # Vérifier le titre
            titre = donnees.get("titre", "")
            if titre and len(titre) > 10 and len(titre) < 60:
                score += 20
                recommendations.append("✅ Titre optimisé (10-60 caractères)")
            else:
                recommendations.append("⚠️  Titre non optimisé")
            
            # Vérifier la description
            description = donnees.get("meta_description", "")
            if description and len(description) > 50 and len(description) < 160:
                score += 20
                recommendations.append("✅ Description optimisée (50-160 caractères)")
            else:
                recommendations.append("⚠️  Description manquante ou non optimisée")
            
            # Vérifier les H1
            h1_count = donnees.get("textes", {}).get("statistiques", {}).get("h1_count", 0)
            if h1_count == 1:
                score += 10
                recommendations.append("✅ 1 seul H1 (parfait)")
            elif h1_count > 1:
                recommendations.append(f"⚠️  {h1_count} H1 détectés (idéal: 1)")
            else:
                recommendations.append("❌ Aucun H1 détecté")
            
            # Vérifier les images
            images = donnees.get("images", {})
            images_sans_alt = [img for img in images.get("images", []) if img.get("alt") in ["", "Pas d'alt"]]
            if images_sans_alt:
                recommendations.append(f"⚠️  {len(images_sans_alt)} images sans attribut alt")
            else:
                score += 10
                recommendations.append("✅ Toutes les images ont un attribut alt")
            
            # Vérifier les liens
            liens = donnees.get("liens", {})
            if liens.get("total", 0) > 0:
                score += 10
                recommendations.append(f"✅ {liens.get('total')} liens trouvés")
            
            # Vérifier la structure
            structure = donnees.get("structure", {})
            if structure.get("frameworks"):
                recommendations.append(f"🛠️  Frameworks détectés: {', '.join(structure['frameworks'])}")
            
            # Calcul final
            score = min(score, 100)
            
            return {
                "url": url,
                "score_seo": score,
                "note": self.obtenir_note(score),
                "recommendations": recommendations,
                "donnees_brutes": donnees
            }
            
        except Exception as e:
            return {"erreur": str(e)}
    
    def obtenir_note(self, score):
        """Convertit un score en note"""
        if score >= 90:
            return "Excellent 🏆"
        elif score >= 70:
            return "Bon 👍"
        elif score >= 50:
            return "Moyen ⚠️"
        else:
            return "À améliorer 🚨"
    
    def exporter_donnees(self, format_type="json"):
        """Exporte les données au format spécifié"""
        if not self.historique:
            return {"erreur": "Aucune donnée à exporter"}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "json":
            filename = f"export_web_{timestamp}.json"
            with open(filename, 'w') as f:
                json.dump(self.historique, f, indent=2)
            return {"succes": True, "fichier": filename}
        
        elif format_type == "csv":
            filename = f"export_web_{timestamp}.csv"
            # Créer un CSV simplifié
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Type", "URL", "Timestamp", "Statut"])
                
                for item in self.historique:
                    writer.writerow([
                        item.get("type", ""),
                        item.get("url", ""),
                        item.get("timestamp", ""),
                        "OK" if "erreur" not in item else "ERREUR"
                    ])
            return {"succes": True, "fichier": filename}
        
        else:
            return {"erreur": f"Format {format_type} non supporté"}

def afficher_menu():
    print("\n" + "="*70)
    print("           🌐 AGENT WEB AVANCÉ V2 - OUTIL PROFESSIONNEL")
    print("="*70)
    print("📋 FONCTIONNALITÉS PRINCIPALES :")
    print("1. 🔍 Scraping web avancé (analyse complète)")
    print("2. 🧪 Test d'API REST (GET, POST, PUT, DELETE)")
    print("3. 👁️  Surveillance de site (temps réel)")
    print("4. 📊 Analyse SEO automatique")
    print("5. 📡 Test de connexion internet")
    print("6. 📜 Historique des analyses")
    print("7. 💾 Exporter les données (JSON/CSV)")
    print("8. ⚙️  Paramètres et informations")
    print("0. 🚪 Quitter")

def installer_dependances():
    """Installe les dépendances nécessaires"""
    print("\n📦 Vérification des dépendances...")
    
    try:
        import requests
        print("✅ requests déjà installé")
    except ImportError:
        print("📦 Installation de requests...")
        os.system(f"{sys.executable} -m pip install requests --quiet")
    
    try:
        from bs4 import BeautifulSoup
        print("✅ beautifulsoup4 déjà installé")
    except ImportError:
        print("📦 Installation de beautifulsoup4...")
        os.system(f"{sys.executable} -m pip install beautifulsoup4 --quiet")
    
    print("✅ Toutes les dépendances sont prêtes !")

def main():
    # Installer les dépendances si nécessaire
    installer_dependances()
    
    agent = AgentWebAvanceV2()
    
    print("🚀 LANCEMENT DE L'AGENT WEB AVANCÉ V2")
    print("Version 2.0 - Outil professionnel de scraping et analyse web")
    
    # Tester la connexion
    print("\n📡 Test de connexion rapide...")
    tests_connexion = agent.verifier_connexion()
    connexion_ok = any(t["statut"] == "✅" for t in tests_connexion)
    
    if connexion_ok:
        print("✅ Connecté à internet")
    else:
        print("⚠️  Mode hors ligne - certaines fonctionnalités seront limitées")
    
    while True:
        afficher_menu()
        
        choix = input("\n👉 Votre choix : ")
        
        if choix == "1":
            url = input("\n🌐 URL à scraper : ").strip()
            if not url:
                print("❌ URL vide")
                continue
            
            profondeur = input("Profondeur de scraping (1-3, défaut: 1) : ").strip()
            if not profondeur:
                profondeur = 1
            else:
                try:
                    profondeur = int(profondeur)
                    if profondeur < 1 or profondeur > 3:
                        print("⚠️  Profondeur limitée à 3, utilisation de 1")
                        profondeur = 1
                except:
                    profondeur = 1
            
            print(f"\n🔍 Début du scraping...")
            resultats = agent.scraper_url(url, profondeur)
            
            if "erreur" in resultats:
                print(f"❌ Erreur : {resultats['erreur']}")
            else:
                print(f"\n✅ SCRAPING RÉUSSI !")
                print(f"📁 URL : {resultats['url']}")
                print(f"📊 Statut : {resultats['status_code']}")
                print(f"⏱️  Temps de réponse : {resultats['temps_reponse']:.2f}s")
                print(f"📏 Taille : {resultats['taille']} octets")
                
                print(f"\n📝 TITRE : {resultats['titre']}")
                print(f"📄 DESCRIPTION : {resultats['meta_description']}")
                print(f"🌐 LANGUE : {resultats['langue']}")
                
                print(f"\n🔗 LIENS : {resultats['liens']['total']} total")
                print(f"   • Internes : {len(resultats['liens']['internes'])}")
                print(f"   • Externes : {len(resultats['liens']['externes'])}")
                
                print(f"\n🖼️  IMAGES : {resultats['images']['total']} images")
                
                print(f"\n📊 STRUCTURE :")
                for elem, count in resultats['structure']['elements'].items():
                    if count > 0:
                        print(f"   • {elem} : {count}")
                
                if resultats['structure']['frameworks']:
                    print(f"🛠️  FRAMEWORKS : {', '.join(resultats['structure']['frameworks'])}")
        
        elif choix == "2":
            print("\n🧪 TEST D'API REST")
            url = input("URL de l'API : ").strip()
            if not url:
                print("❌ URL vide")
                continue
            
            method = input("Méthode (GET/POST/PUT/DELETE, défaut: GET) : ").strip().upper()
            if method not in ["GET", "POST", "PUT", "DELETE"]:
                method = "GET"
            
            data = None
            if method in ["POST", "PUT"]:
                data_input = input("Données JSON (optionnel, ex: {\"key\":\"value\"}) : ").strip()
                if data_input:
                    try:
                        data = json.loads(data_input)
                    except:
                        print("⚠️  JSON invalide, utilisation sans données")
            
            print(f"\n🔍 Test de l'API avec méthode {method}...")
            resultats = agent.tester_api(url, method, data)
            
            if "erreur" in resultats:
                print(f"❌ Erreur : {resultats['erreur']}")
            else:
                print(f"\n✅ TEST API RÉUSSI !")
                print(f"📡 URL : {resultats['url']}")
                print(f"⚡ Méthode : {resultats['method']}")
                print(f"📊 Statut : {resultats['status_code']}")
                print(f"⏱️  Temps de réponse : {resultats['temps_reponse']}")
                print(f"📏 Taille : {resultats['taille']} octets")
                print(f"📄 Type de contenu : {resultats['content_type']}")
                
                if "body" in resultats:
                    print(f"\n📦 RÉPONSE JSON :")
                    print(f"   {json.dumps(resultats['body'], indent=2)[:200]}...")
                elif "body_preview" in resultats:
                    print(f"\n📄 PRÉVISUALISATION RÉPONSE :")
                    print(f"   {resultats['body_preview'][:200]}...")
        
        elif choix == "3":
            print("\n👁️  SURVEILLANCE DE SITE")
            url = input("URL à surveiller : ").strip()
            if not url:
                print("❌ URL vide")
                continue
            
            interval = input("Intervalle en secondes (défaut: 30) : ").strip()
            if not interval:
                interval = 30
            else:
                try:
                    interval = int(interval)
                except:
                    interval = 30
            
            duree = input("Durée totale en secondes (défaut: 300) : ").strip()
            if not duree:
                duree = 300
            else:
                try:
                    duree = int(duree)
                except:
                    duree = 300
            
            print(f"\n🚀 Lancement de la surveillance...")
            stats = agent.surveiller_site(url, interval, duree)
            
            print(f"\n📊 RAPPORT DE SURVEILLANCE :")
            print(f"📁 URL : {stats['url']}")
            print(f"⏱️  Début : {stats['debut']}")
            print(f"📈 Fin : {stats['statistiques'].get('fin', 'N/A')}")
            print(f"🔄 Total tests : {stats['statistiques'].get('total_tests', 0)}")
            print(f"✅ Tests réussis : {stats['statistiques'].get('tests_succes', 0)}")
            print(f"📊 Taux de réussite : {stats['statistiques'].get('taux_succes', '0%')}")
            print(f"⏳ Durée totale : {stats['statistiques'].get('duree_totale', '0s')}")
        
        elif choix == "4":
            url = input("\n🔍 URL à analyser (SEO) : ").strip()
            if not url:
                print("❌ URL vide")
                continue
            
            print(f"\n📊 Analyse SEO en cours...")
            analyse = agent.analyser_seo(url)
            
            if "erreur" in analyse:
                print(f"❌ Erreur : {analyse['erreur']}")
            else:
                print(f"\n📈 RAPPORT SEO COMPLET")
                print(f"🌐 URL : {analyse['url']}")
                print(f"🏆 SCORE : {analyse['score_seo']}/100")
                print(f"📊 NOTE : {analyse['note']}")
                
                print(f"\n💡 RECOMMANDATIONS :")
                for rec in analyse['recommendations']:
                    print(f"   • {rec}")
                
                # Afficher quelques détails
                donnees = analyse.get('donnees_brutes', {})
                if donnees:
                    print(f"\n📝 INFORMATIONS DÉTECTÉES :")
                    print(f"   • Titre : {donnees.get('titre', 'N/A')[:50]}...")
                    print(f"   • Description : {donnees.get('meta_description', 'N/A')[:50]}...")
                    print(f"   • Images : {donnees.get('images', {}).get('total', 0)}")
                    print(f"   • Liens : {donnees.get('liens', {}).get('total', 0)}")
        
        elif choix == "5":
            print("\n📡 TEST DE CONNEXION INTERNET")
            resultats = agent.verifier_connexion()
            
            print(f"\n🔌 RÉSULTATS DES TESTS :")
            for test in resultats:
                print(f"   • {test['service']} : {test['statut']} ({test.get('temps', 'N/A')})")
            
            # Résumé
            succes = sum(1 for t in resultats if t["statut"] == "✅")
            print(f"\n📊 RÉSUMÉ : {succes}/{len(resultats)} services accessibles")
        
        elif choix == "6":
            if not agent.historique:
                print("\n📭 Historique vide")
            else:
                print(f"\n📜 HISTORIQUE DES ANALYSES ({len(agent.historique)})")
                print("-" * 60)
                
                for i, item in enumerate(agent.historique[-10:], 1):
                    date = datetime.fromisoformat(item['timestamp']).strftime('%H:%M')
                    type_emoji = {
                        "scraping": "🔍",
                        "api_test": "🧪",
                        "surveillance": "👁️"
                    }.get(item.get('type', ''), '📄')
                    
                    print(f"{i}. [{date}] {type_emoji} {item.get('type', 'inconnu').upper()}")
                    print(f"   📍 {item.get('url', 'N/A')[:50]}...")
                    
                    if "erreur" in item:
                        print(f"   ❌ Erreur")
                    else:
                        print(f"   ✅ Succès")
                    
                    print()
        
        elif choix == "7":
            print("\n💾 EXPORTATION DES DONNÉES")
            print("1. Format JSON (recommandé)")
            print("2. Format CSV (simple)")
            
            format_choix = input("Format : ").strip()
            
            if format_choix == "1":
                resultat = agent.exporter_donnees("json")
            elif format_choix == "2":
                resultat = agent.exporter_donnees("csv")
            else:
                print("❌ Choix invalide")
                continue
            
            if "erreur" in resultat:
                print(f"❌ {resultat['erreur']}")
            else:
                print(f"✅ Données exportées avec succès !")
                print(f"📁 Fichier : {resultat['fichier']}")
                print(f"📊 {len(agent.historique)} entrées exportées")
        
        elif choix == "8":
            print("\n⚙️  INFORMATIONS SUR L'AGENT :")
            print(f"Version : 2.0 (Web Avancé)")
            print(f"Analyses enregistrées : {len(agent.historique)}")
            print(f"Fichier de logs : {agent.log_file}")
            print(f"User-Agent : {agent.session.headers['User-Agent'][:50]}...")
            
            # Tests de connexion rapides
            print(f"\n📡 ÉTAT CONNEXION :")
            tests = agent.verifier_connexion()
            for test in tests:
                print(f"   • {test['service']} : {test['statut']}")
        
        elif choix == "0":
            print("\n👋 Au revoir ! Agent web terminé.")
            if agent.historique:
                print(f"📊 Résumé : {len(agent.historique)} analyses enregistrées")
            break
        
        else:
            print("❌ Choix invalide")
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
EOF

# Rendre exécutable
chmod +x agent_web_avance_v2.py

# Tester l'agent
python3 agent_web_avance_v2.py
