cat > test_app.py << 'EOF'
#!/usr/bin/env python3
"""
Tests unitaires pour l'application Flask
"""

import unittest
import json
import os
import sys

# Ajouter le répertoire courant au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
    has_app = True
except ImportError:
    has_app = False
    print("⚠️ Module 'app' non trouvé, tests Flask ignorés")

class FlaskTestCase(unittest.TestCase):
    
    def setUp(self):
        """Configuration avant chaque test"""
        if has_app:
            self.app = app.test_client()
            self.app.testing = True
    
    def test_index(self):
        """Test de la route principale"""
        if not has_app:
            self.skipTest("Module 'app' non disponible")
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_status(self):
        """Test de l'API status"""
        if not has_app:
            self.skipTest("Module 'app' non disponible")
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_get_tasks(self):
        """Test de récupération des tâches"""
        if not has_app:
            self.skipTest("Module 'app' non disponible")
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
    
    def test_create_task(self):
        """Test de création d'une tâche"""
        if not has_app:
            self.skipTest("Module 'app' non disponible")
        response = self.app.post('/api/tasks',
                                data=json.dumps({'title': 'Test task'}),
                                content_type='application/json')
        self.assertIn(response.status_code, [200, 201])
    
    def test_increment_counter(self):
        """Test d'incrémentation du compteur"""
        if not has_app:
            self.skipTest("Module 'app' non disponible")
        response = self.app.post('/api/counter/increment')
        self.assertEqual(response.status_code, 200)

class DatabaseTestCase(unittest.TestCase):
    
    def test_database_operations(self):
        """Test des opérations de base de données"""
        try:
            import database
            # Test d'initialisation
            db_path = database.init_database()
            self.assertTrue(os.path.exists(db_path))
            print(f"✅ Base de données: {db_path}")
            
        except ImportError:
            self.skipTest("Module 'database' non trouvé")

def run_all_tests():
    """Exécuter tous les tests"""
    print("\n" + "="*60)
    print("🧪 EXÉCUTION DE TOUS LES TESTS")
    print("="*60)
    
    # Tests unitaires
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Ajouter les tests Flask
    if has_app:
        suite.addTests(loader.loadTestsFromTestCase(FlaskTestCase))
    
    # Ajouter les tests base de données
    suite.addTests(loader.loadTestsFromTestCase(DatabaseTestCase))
    
    # Exécuter
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*60)
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ Tous les tests passent avec succès !")
    else:
        print("❌ Certains tests ont échoué")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_all_tests()
EOF
