# generate_report.py
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Rapport Flask</title>
</head>
<body>
    <h1>Serveur Flask fonctionnel</h1>
    <p>Date: """ + __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
</body>
</html>
"""

with open('/root/Documents/flask_report.html', 'w') as f:
    f.write(html_content)

print("Rapport HTML généré avec succès")
