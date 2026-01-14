#!/usr/bin/env python3

def main():
    print("=== Agent IA Gratuit ===")
    print("1. Traiter un email")
    print("2. Planifier un rendez-vous")
    print("3. Transcrire une note vocale")
    print("4. Afficher les statistiques")
    
    choix = input("Votre choix (1-4) : ")
    
    if choix == "1":
        expediteur = input("Expéditeur : ")
        sujet = input("Sujet : ")
        print(f"Email de {expediteur} traité : {sujet}")
    
    elif choix == "2":
        titre = input("Titre du rendez-vous : ")
        date = input("Date (JJ/MM/AAAA) : ")
        print(f"Rendez-vous '{titre}' planifié le {date}")
    
    elif choix == "3":
        print("Transcription simulée : 'Réunion importante demain à 10h'")
    
    elif choix == "4":
        print("Statistiques : 3 emails, 2 rendez-vous, 1 note vocale")
    
    else:
        print("Choix invalide")

if __name__ == "__main__":
    main()
