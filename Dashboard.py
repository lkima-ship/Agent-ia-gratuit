# Dans dashboard.py
class Dashboard:
    def __init__(self):
        self.metrics = {
            'requests_processed': 0,
            'avg_response_time': 0,
            'user_satisfaction': 0,
            'active_tasks': []
        }
    
    def update_metrics(self, agent_activity):
        """Met à jour les métriques en temps réel"""
        self.metrics['requests_processed'] += 1
        # Logique de mise à jour...
    
    def generate_report(self):
        """Génère un rapport détaillé"""
        return {
            'performance': self.calculate_performance(),
            'insights': self.extract_insights(),
            'recommendations': self.generate_recommendations()
        }
