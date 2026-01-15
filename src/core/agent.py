#!/usr/bin/env python3
from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Agent IA Gratuit</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .option { margin: 10px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Agent IA Gratuit</h1>
    <p>Assistant intelligent pour automatiser vos tâches</p>
    
    <form method="POST" action="/">
        <div class="option">
            <h3>Option 1: Traiter un email</h3>
            <input type="hidden" name="choix" value="1">
            <button type="submit">Exécuter</button>
        </div>
    </form>
    
    <form method="POST" action="/">
        <div class="option">
            <h3>Option 2: Planifier un rendez-vous</h3>
            <input type="hidden" name="choix" value="2">
            <button type="submit">Exécuter</button>
        </div>
    </form>
    
    <form method="POST" action="/">
        <div class="option">
            <h3>Option 3: Transcrire note vocale</h3>
            <input type="hidden" name="choix" value="3">
            <button type="submit">Exécuter</button>
        </div>
    </form>
    
    <form method="POST" action="/">
        <div class="option">
            <h3>Option 4: Voir les statistiques</h3>
            <input type="hidden" name="choix" value="4">
            <button type="submit">Exécuter</button>
        </div>
    </form>
    
    {% if result %}
    <div class="result">
        <h3>Résultat :</h3>
        <pre>{{ result }}</pre>
    </div>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        choix = request.form.get('choix', '1')
        
        if choix == "1":
            result = "Email traité avec succès\n- Expéditeur: exemple@test.com\n- Sujet: Réunion importante"
        elif choix == "2":
            result = "Rendez-vous planifié\n- Titre: Réunion équipe\n- Date: 15/01/2024"
        elif choix == "3":
            result = "Transcription simulée :\n'Réunion importante demain à 10h. Préparez les rapports.'"
        elif choix == "4":
            result = "Statistiques :\n- 3 emails en attente\n- 2 rendez-vous cette semaine\n- 1 note vocale non transcrite"
    
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
