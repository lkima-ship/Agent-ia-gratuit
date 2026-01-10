# Supprimer l'ancien fichier
rm -f menu.py

# Créer un nouveau menu.py
echo 'print("=== AGENT IA GRATUIT ===")' > menu.py
echo 'print("1. Démarrer le serveur")' >> menu.py
echo 'print("2. Tester l installation")' >> menu.py
echo 'print("3. Quitter")' >> menu.py
echo 'print("========================")' >> menu.py
echo 'try:' >> menu.py
echo '    choix = input("Choix: ")' >> menu.py
echo '    print(f"Vous avez choisi: {choix}")' >> menu.py
echo 'except KeyboardInterrupt:' >> menu.py
echo '    print("\nInterruption")' >> menu.py
