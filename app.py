# Dans agent_ia_pro.py ou agent.py
import asyncio
from typing import Dict, Any
import json
from datetime import datetime

class IntelligentAgent:
    def __init__(self):
        self.context = {}
        self.skills = {
            'email': EmailProcessor(),
            'calendar': CalendarManager(),
            'voice': VoiceTranscriber(),
            'analysis': DataAnalyzer()
        }
        self.memory = AgentMemory()
    
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Traite une requête utilisateur intelligemment"""
        
        # Analyse de l'intention
        intent = await self.detect_intent(user_input)
        
        # Exécution de la compétence appropriée
        if intent == "email":
            return await self.skills['email'].process(user_input)
        elif intent == "schedule":
            return await self.skills['calendar'].manage_appointment(user_input)
        # ...
        
        return {"response": "Je n'ai pas compris votre demande"}
    
    async def learn_from_interaction(self, feedback: Dict):
        """Apprentissage automatique des préférences"""
        self.memory.update(feedback)
        # Dans agent_ia_pro.py ou agent.py
import asyncio
from typing import Dict, Any
import json
from datetime import datetime

class IntelligentAgent:
    def __init__(self):
        self.context = {}
        self.skills = {
            'email': EmailProcessor(),
            'calendar': CalendarManager(),
            'voice': VoiceTranscriber(),
            'analysis': DataAnalyzer()
        }
        self.memory = AgentMemory()
    
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Traite une requête utilisateur intelligemment"""
        
        # Analyse de l'intention
        intent = await self.detect_intent(user_input)
        
        # Exécution de la compétence appropriée
        if intent == "email":
            return await self.skills['email'].process(user_input)
        elif intent == "schedule":
            return await self.skills['calendar'].manage_appointment(user_input)
        # ...
        
        return {"response": "Je n'ai pas compris votre demande"}
    
    async def learn_from_interaction(self, feedback: Dict):
        """Apprentissage automatique des préférences"""
        self.memory.update(feedback)
        # Dans app.py - Version améliorée
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Endpoints principaux
@app.route('/api/v1/process', methods=['POST'])
def process_endpoint():
    data = request.json
    agent_response = process_with_agent(data['query'])
    return jsonify({
        'success': True,
        'response': agent_response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v1/emails/analyze', methods=['POST'])
def analyze_email():
    """Analyse sémantique d'un email"""
    email_text = request.json['email']
    sentiment = analyze_sentiment(email_text)
    urgency = detect_urgency(email_text)
    
    return jsonify({
        'sentiment': sentiment,
        'urgency_level': urgency,
        'suggested_actions': generate_suggestions(email_text)
    })

@app.route('/api/v1/calendar/smart-schedule', methods=['POST'])
def smart_schedule():
    """Planification intelligente de rendez-vous"""
    constraints = request.json['constraints']
    optimal_time = find_optimal_time(constraints)
    
    return jsonify({
        'suggested_time': optimal_time,
        'conflicts': check_conflicts(optimal_time),
        'duration_recommendation': suggest_duration(constraints)
    })
        
