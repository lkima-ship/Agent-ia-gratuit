echo '#!/usr/bin/env python3' > main.py
echo '' >> main.py
echo 'print("🤖 AGENT IA GRATUIT")' >> main.py
echo 'print("===================")' >> main.py
echo 'print("Bienvenue!")' >> main.py
echo '' >> main.py
echo 'print("Options:")' >> main.py
echo 'print("1. Démarrer le serveur")' >> main.py
echo 'print("2. Tester")' >> main.py
echo 'print("3. Quitter")' >> main.py
echo '' >> main.py
echo 'try:' >> main.py
echo '    choix = input("Votre choix (1-3): ")' >> main.py
echo '    print(f"Vous avez choisi: {choix}")' >> main.py
echo '    if choix == "1":' >> main.py
echo '        print("Lancement du serveur...")' >> main.py
echo '        import subprocess' >> main.py
echo '        subprocess.run(["python3", "server.py"])' >> main.py
echo '    elif choix == "2":' >> main.py
echo '        print("Test réussi!")' >> main.py
echo '    elif choix == "3":' >> main.py
echo '        print("Au revoir!")' >> main.py
echo '    else:' >> main.py
echo '        print("Choix invalide")' >> main.py
echo 'except KeyboardInterrupt:' >> main.py
echo '    print("\nInterruption")' >> main.py
