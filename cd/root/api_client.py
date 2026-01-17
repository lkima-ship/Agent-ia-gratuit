cat > /root/api_client.py << 'EOF'
#!/usr/bin/env python3
"""
Client de test pour l'API REST
"""

import requests
import sys

API_URL = "http://localhost:5002"
API_KEYS = {
    "admin": "admin_key_123",
    "user": "user_key_456"
}

def test_api(api_key, key_type="user"):
    """Teste les endpoints de l'API"""
    headers = {"X-API-Key": api_key}
    
    print(f"\n🔧 Test avec clé {key_type}...")
    
    # Test statut
    try:
        response = requests.get(f"{API_URL}/api/status", headers=headers)
        print(f"GET /api/status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"   Erreur: {e}")
    
    # Test système (admin uniquement)
    if key_type == "admin":
        try:
            response = requests.get(f"{API_URL}/api/system", headers=headers)
            print(f"GET /api/system: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"   CPU: {data.get('cpu_percent')}%")
                print(f"   Mémoire: {data.get('memory_percent')}%")
        except Exception as e:
            print(f"   Erreur: {e}")
    
    # Test echo
    try:
        data = {"test": "données", "number": 42}
        response = requests.post(f"{API_URL}/api/echo", 
                                json=data, 
                                headers=headers)
        print(f"POST /api/echo: {response.status_code}")
        if response.status_code == 200:
            print(f"   Réponse: {response.json()}")
    except Exception as e:
        print(f"   Erreur: {e}")

if __name__ == "__main__":
    print("🧪 Client de test API REST")
    print(f"URL: {API_URL}")
    
    # Tester sans clé
    print("\n🔓 Test sans authentification...")
    try:
        response = requests.get(f"{API_URL}/api/docs")
        print(f"GET /api/docs: {response.status_code}")
    except Exception as e:
        print(f"   Erreur: {e}. L'API est-elle démarrée?")
    
    # Tester avec clé user
    test_api(API_KEYS["user"], "user")
    
    # Tester avec clé admin
    test_api(API_KEYS["admin"], "admin")
    
    print("\n✅ Tests terminés")
EOF
