cat > /root/api_client_final.py << 'EOF'
#!/usr/bin/env python3
"""
Client Python pour l'API Agents IA
"""

import requests
import json

API_BASE = "http://localhost:5002"

def test_api():
    print("🧪 Test de l'API Agents IA")
    print("=" * 40)
    
    # Test 1: Accueil
    try:
        resp = requests.get(f"{API_BASE}/")
        print(f"GET / → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Système: {data.get('system')}")
            print(f"   Version: {data.get('version')}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 2: Agents
    try:
        resp = requests.get(f"{API_BASE}/api/agents")
        print(f"\nGET /api/agents → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Agents trouvés: {data.get('total', 0)}")
            for agent in data.get('agents', []):
                print(f"   • {agent}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test 3: Statut
    try:
        resp = requests.get(f"{API_BASE}/api/status")
        print(f"\nGET /api/status → {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Status: {data.get('status')}")
            print(f"   Time: {data.get('time')}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    print("\n" + "=" * 40)
    print("✅ Tests terminés")

if __name__ == "__main__":
    test_api()
EOF

# Tester le client
python3 /root/api_client_final.py
