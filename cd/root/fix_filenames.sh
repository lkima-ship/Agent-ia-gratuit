cat > /root/fix_filenames.sh << 'EOF'
#!/bin/sh
echo "🔧 CORRECTION DES NOMS DE FICHIERS"
echo "=================================="

# Liste des corrections à faire
CORRECTIONS="
web_b_interface.py:web_interface.py
agent_ia_ml.py:agent_ia_ml.py
agent_analyse_donnees.py:agent_analyse_donnees.py
agent_surveillance.py:agent_surveillance.py
"

echo ""
echo "📁 ÉTAT ACTUEL DES FICHIERS :"
ls -la /root/*.py | grep -E "(web|agent|cognitif)" | head -10

echo ""
echo "🔄 CORRECTIONS À APPLIQUER :"

# Correction 1: web_b_interface.py -> web_interface.py
if [ -f "/root/web_b_interface.py" ]; then
    echo "  • Renommage: web_b_interface.py → web_interface.py"
    mv /root/web_b_interface.py /root/web_interface.py
fi

# Correction 2: Vérifier/créer agent_cognitif.py
if [ ! -f "/root/agent_cognitif.py" ]; then
    echo "  • Création: agent_cognitif.py"
    cat > /root/agent_cognitif.py << 'PYEOF'
#!/usr/bin/env python3
"""
AGENT COGNITIF - Alpine Linux
Version simplifiée mais fonctionnelle
"""
import json
import time
import os

class CognitiveAgent:
    def __init__(self):
        self.memory_file = "/root/cognitive_memory.json"
        self.load_memory()
    
    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
        else:
            self.memory = {"knowledge": [], "decisions": []}
    
    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def learn(self, fact, category="general"):
        self.memory["knowledge"].append({
            "fact": fact,
            "category": category,
            "timestamp": time.time()
        })
        self.save_memory()
        return f"✅ Appris: {fact}"
    
    def recall(self, category=None):
        if category:
            items = [k for k in self.memory["knowledge"] if k["category"] == category]
        else:
            items = self.memory["knowledge"]
        return items
    
    def analyze(self, query):
        if "apprend" in query.lower():
            return "Je peux apprendre. Dites-moi ce que je dois retenir."
        elif "souviens" in query.lower():
            return f"J'ai {len(self.memory['knowledge'])} connaissances en mémoire."
        elif "aide" in query.lower():
            return "Je peux: apprendre, me souvenir, analyser."
        else:
            return f"J'ai analysé: '{query}'. Que souhaitez-vous faire?"

def main():
    print("🧠 AGENT COGNITIF INTELLIGENT")
    print("=" * 40)
    
    agent = CognitiveAgent()
    print(f"💾 Mémoire: {len(agent.memory['knowledge'])} faits")
    
    while True:
        print("\n1. 💬 Interagir avec l'agent")
        print("2. 📚 Voir la mémoire")
        print("3. 📊 Statistiques")
        print("0. 🚪 Quitter")
        
        choice = input("\n👉 Votre choix: ")
        
        if choice == "1":
            query = input("\n💭 Votre question: ")
            response = agent.analyze(query)
            print(f"\n🤖 {response}")
            
            # Apprentissage automatique
            if "?" not in query and len(query.split()) > 3:
                agent.learn(f"Question: {query}", "interaction")
                print("📝 Enregistré dans la mémoire")
        
        elif choice == "2":
            print("\n📚 CONTENU DE LA MÉMOIRE:")
            knowledge = agent.recall()
            for i, item in enumerate(knowledge[-5:], 1):
                print(f"{i}. {item['fact'][:50]}... ({item['category']})")
        
        elif choice == "3":
            print(f"\n📊 STATISTIQUES:")
            print(f"• Connaissances: {len(agent.memory['knowledge'])}")
            print(f"• Décisions: {len(agent.memory['decisions'])}")
            print(f"• Fichier: {agent.memory_file}")
        
        elif choice == "0":
            print("\n👋 Session terminée. Au revoir!")
            break
        
        input("\n↵ Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()
PYEOF
fi

# Donner les permissions
chmod +x /root/*.py 2>/dev/null

echo ""
echo "✅ CORRECTIONS APPLIQUÉES"
echo ""
echo "📋 FICHIERS DISPONIBLES :"
ls -la /root/web_interface.py /root/agent_cognitif.py /root/agent_ia_ml.py 2>/dev/null

echo ""
echo "🚀 POUR LANCER :"
echo "  python3 /root/web_interface.py"
echo "  python3 /root/agent_cognitif.py"
echo "  python3 /root/agent_ia_ml.py"
EOF

chmod +x /root/fix_filenames.sh
/root/fix_filenames.sh
