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
        
