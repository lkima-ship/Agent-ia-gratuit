"""
Module IA Gratuit - Google Gemini API
"""

import os
import google.generativeai as genai
import whisper

class FreeAIProcessor:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def generate_email_response(self, email_content, subject, sender):
        """Génère une réponse d'email"""
        
        if not self.model:
            return "Merci pour votre email. Je vous répondrai bientôt."
        
        prompt = f"""
        Réponds à cet email professionnellement:
        
        De: {sender}
        Sujet: {subject}
        Contenu: {email_content[:1000]}
        
        Règles:
        1. Style professionnel mais amical
        2. Si demande de rendez-vous, propose 2 créneaux
        3. Maximum 150 mots
        4. En français
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Merci pour votre message. Je traite votre demande."
    
    def transcribe_audio(self, audio_file):
        """Transcrit un fichier audio gratuitement"""
        try:
            model = whisper.load_model("base")
            result = model.transcribe(audio_file, language="fr")
            return result["text"]
        except:
            return "Erreur de transcription"
