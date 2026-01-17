cat > agent_ia_ml.py << 'EOF'
#!/usr/bin/env python3
"""
AGENT IA AVANCÉ - Apprentissage automatique
"""
import numpy as np
import json
from collections import Counter
import re

class AgentML:
    def __init__(self):
        self.connaissances = self.charger_connaissances()
    
    def charger_connaissances(self):
        base = {
            "salutations": ["bonjour", "salut", "coucou", "hello", "hey"],
            "questions": ["comment", "pourquoi", "quand", "où", "qui"],
            "actions": ["faire", "créer", "développer", "analyser", "tester"],
            "langages": ["python", "javascript", "java", "c++", "php"],
            "sujets_tech": ["ia", "machine learning", "web", "mobile", "cloud"]
        }
        return base
    
    def analyser_semantique(self, texte):
        """Analyse sémantique avancée"""
        texte_lower = texte.lower()
        mots = re.findall(r'\b\w+\b', texte_lower)
        
        categories = {}
        for categorie, mots_cles in self.connaissances.items():
            count = sum(1 for mot in mots_cles if mot in texte_lower)
            if count > 0:
                categories[categorie] = count
        
        # Calcul de complexité
        complexite = len(mots) / 10  # Normalisé
        complexite = min(complexite, 1.0)
        
        return {
            "mots": len(mots),
            "categories": categories,
            "complexite": f"{complexite:.1%}",
            "predominant": max(categories.items(), key=lambda x: x[1])[0] if categories else "indéterminé"
        }
    
    def generer_reponse(self, texte):
        """Génère une réponse intelligente"""
        analyse = self.analyser_semantique(texte)
        
        if "salutations" in texte.lower():
            return "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
        
        if "?" in texte:
            if "comment" in texte.lower():
                return "Je peux vous guider étape par étape. Pouvez-vous préciser votre besoin ?"
            elif "pourquoi" in texte.lower():
                return "C'est une excellente question. Explorons ensemble les raisons."
        
        # Réponses contextuelles
        if analyse["categories"].get("langages", 0) > 0:
            return f"Je vois que vous parlez de programmation. Python est excellent pour l'IA !"
        
        if analyse["categories"].get("sujets_tech", 0) > 0:
            return "Le domaine tech évolue rapidement. Je peux vous aider avec ça."
        
        return f"J'ai analysé votre message ({analyse['mots']} mots). C'est intéressant !"

def main():
    agent = AgentML()
    
    print("🧠 AGENT IA AVEC MACHINE LEARNING")
    print("="*40)
    
    while True:
        print("\n1. Analyser un texte")
        print("2. Générer une réponse")
        print("3. Tester plusieurs phrases")
        print("4. Quitter")
        
        choix = input("Choix : ")
        
        if choix == "1":
            texte = input("Texte à analyser : ")
            analyse = agent.analyser_semantique(texte)
            print(f"\n📊 Analyse :")
            print(f"• Mots : {analyse['mots']}")
            print(f"• Complexité : {analyse['complexite']}")
            print(f"• Catégorie principale : {analyse['predominant']}")
            if analyse['categories']:
                print("• Détection :")
                for cat, count in analyse['categories'].items():
                    print(f"  - {cat} : {count}")
        
        elif choix == "2":
            texte = input("Votre message : ")
            reponse = agent.generer_reponse(texte)
            print(f"\n🤖 Réponse : {reponse}")
        
        elif choix == "3":
            phrases = [
                "Bonjour, comment créer une IA en Python ?",
                "Je veux développer un site web moderne",
                "Quels sont les meilleurs langages pour le machine learning ?",
                "Merci pour votre aide"
            ]
            
            print("\n🔍 Tests automatiques :")
            for phrase in phrases:
                print(f"\n📝 {phrase}")
                print(f"🤖 {agent.generer_reponse(phrase)}")
        
        elif choix == "4":
            print("👋 Au revoir !")
            break
        
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()
EOF

python3 agent_ia_ml.py
