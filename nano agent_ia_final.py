#!/usr/bin/env python3
# Agent IA Gratuit - Version avec boucle

import os
import time

def effacer_ecran():
    os.system('clear' if os.name == 'posix' else 'cls')

def traiter_email():
    print("\n📧 TRAITEMENT D'EMAIL")
    print("-" * 30)
    sujet = input("Sujet de l'email: ")
    expediteur = input("Expéditeur: ")
    print(f"\n✅ Email '{sujet}' de {expediteur} traité avec succès!")
    time.sleep(1)

def planifier_rendezvous():
    print("\n📅 PLANIFICATION DE RENDEZ-VOUS")
    print("-" * 30)
    titre = input("Titre du rendez-vous: ")
    date = input("Date (JJ/MM/AAAA): ")
    heure = input("Heure (HH:MM): ")
    lieu = input("Lieu: ")
    print(f"\n✅ Rendez-vous '{titre}' planifié le {date} à {heure} à {lieu}!")
    time.sleep(1)

def transcrire_note_vocale():
    print("\n🎤 TRANSCRIPTION DE NOTE VOCALE")
    print("-" * 30)
    print("Simulation de transcription...")
    transcription = "Réunion importante demain à 10h avec l'équipe projet"
    print(f"\n📝 Transcription: '{transcription}'")
    time.sleep(1)

def afficher_statistiques():
    print("\n📊 STATISTIQUES")
    print("-" * 30)
    print("📧 Emails: 3")
    print("📅 Rendez-vous: 2")
    print("🎤 Notes vocales: 1")
    print("-" * 30)
    time.sleep(2)

def main():
    """Fonction principale avec boucle"""
    while True:
        effacer_ecran()
        print("=" * 40)
        print("🤖 AGENT IA GRATUIT")
        print("=" * 40)
        print("1. Traiter un email")
        print("2. Planifier un rendez-vous")
        print("3. Transcrire une note vocale")
        print("4. Afficher les statistiques")
        print("5. Mode commandes avancées")
        print("0. Quitter")
        print("=" * 40)
        
        try:
            choix = input("\nVotre choix (0-5): ").strip()
            
            if choix == "1":
                traiter_email()
            elif choix == "2":
                planifier_rendezvous()
            elif choix == "3":
                transcrire_note_vocale()
            elif choix == "4":
                afficher_statistiques()
            elif choix == "5":
                mode_commandes_avancees()
            elif choix == "0":
                print("\n👋 Au revoir !")
                break
            else:
                print("\n❌ Choix invalide ! Veuillez choisir entre 0 et 5.")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 Interruption - Au revoir !")
            break
        except Exception as e:
            print(f"\n⚠️  Erreur: {e}")
            time.sleep(2)

def mode_commandes_avancees():
    """Mode commandes texte avancées"""
    while True:
        effacer_ecran()
        print("=" * 40)
        print("🔧 MODE COMMANDES AVANCÉES")
        print("=" * 40)
        print("Commandes disponibles:")
        print("  detail rdv    - Détails des rendez-vous")
        print("  liste emails  - Liste des emails")
        print("  recherche mot - Recherche par mot-clé")
        print("  aide          - Afficher l'aide")
        print("  retour        - Retour au menu principal")
        print("=" * 40)
        
        commande = input("\nCommande: ").strip().lower()
        
        if commande == "retour":
            break
        elif commande == "detail rdv":
            print("\n📅 DÉTAILS DES RENDEZ-VOUS:")
            print("  • Réunion projet - 16/01 - 10:00 - Salle A")
            print("  • Dentiste - 18/01 - 14:30 - Cabinet médical")
            input("\nAppuyez sur Entrée pour continuer...")
        elif commande == "liste emails":
            print("\n📧 LISTE DES EMAILS:")
            print("  1. Réunion projet - alice@entreprise.com")
            print("  2. Facture #12345 - billing@fournisseur.fr")
            print("  3. Newsletter Tech - news@tech.com")
            input("\nAppuyez sur Entrée pour continuer...")
        elif commande.startswith("recherche "):
            mot = commande.split(" ", 1)[1]
            print(f"\n🔍 RECHERCHE: '{mot}'")
            print("  Résultats trouvés: 2 emails, 1 rendez-vous")
            input("\nAppuyez sur Entrée pour continuer...")
        elif commande == "aide":
            print("\nℹ️  AIDE:")
            print("  Tapez les commandes telles qu'elles apparaissent")
            print("  Utilisez 'retour' pour revenir au menu principal")
            input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("\n❌ Commande non reconnue. Tapez 'aide' pour l'aide.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption - Au revoir !")
