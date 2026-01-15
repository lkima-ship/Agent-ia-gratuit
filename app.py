#!/usr/bin/env python3
from flask import Flask, jsonify, request
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Agent IA Gratuit</title></head>
    <body>
        <h1>Agent IA Gratuit - API</h1>
        <p>API en cours d'exécution...</p>
        <p>Endpoints disponibles :</p>
        <ul>
            <li>GET /status - Vérifier le statut</li>
            <li>POST /execute - Exécuter une commande</li>
        </ul>
    </body>
    </html>
    '''

@app.route('/status')
def status():
    return jsonify({
        "status": "en ligne",
        "service": "Agent IA Gratuit API",
        "port": 5000
    })

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    choix = data.get('choix', '1')
    
    # Simuler l'exécution du script agent.py
    resultats = {
        "1": "Email traité avec succès",
        "2": "Rendez-vous planifié",
        "3": "Transcription générée",
        "4": "Statistiques affichées"
    }
    
    return jsonify({
        "choix": choix,
        "resultat": resultats.get(choix, "Choix invalide"),
        "message": "Commande exécutée avec succès"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
