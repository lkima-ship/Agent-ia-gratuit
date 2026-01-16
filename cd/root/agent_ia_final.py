#!/usr/bin/env python3
# Agent IA Gratuit - Version avec boucle

import os

while True:
    os.system('clear')
    print("=== Agent IA Gratuit ===")
    print("1. Traiter un email")
    print("2. Planifier un rendez-vous")
    print("3. Transcrire une note vocale")
    print("4. Afficher les statistiques")
    print("0. Quitter")
    
    choix = input("\nVotre choix (0-4) : ")
    
    if choix == "1":
        print("\n=== Traiter un email ===")
        expediteur = input("Expediteur : ")
        sujet = input("Sujet : ")
        print(f"\nEmail de {expediteur} traite : {sujet}")
        input("\nAppuyez sur Entree pour continuer...")
    
    elif choix == "2":
        print("\n=== Planifier un rendez-vous ===")
        titre = input("Titre du rendez-vous : ")
        date = input("Date (JJ/MM/AAAA) : ")
        print(f"\nRendez-vous '{titre}' planifie le {date}")
        input("\nAppuyez sur Entree pour continuer...")
    
    elif choix == "3":
        print("\n=== Transcrire une note vocale ===")
        print("Transcription simulee : 'Reunion importante demain a 10h'")
        input("\nAppuyez sur Entree pour continuer...")
    
    elif choix == "4":
        print("\n=== Statistiques ===")
        print("Statistiques : 3 emails, 2 rendez-vous, 1 note vocale")
        input("\nAppuyez sur Entree pour continuer...")
    
    elif choix == "0":
        print("\nAu revoir!")
        break
    
    else:
        print("\nChoix invalide!")
        input("Appuyez sur Entree pour continuer...")
