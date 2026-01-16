# Créer une nouvelle version corrigée
cat > agent_ia_final.py << 'EOF'
#!/usr/bin/env python3
# Agent IA Gratuit - Version corrigée avec boucle

import os

def effacer_ecran():
    os.system('clear')

def traiter_email():
    print("\n📧 TRAITEMENT D'EMAIL")
    print("-" * 30)
    expediteur = input("Expéditeur : ")
    sujet = input("Sujet : ")
    print(f"\n✅ Email de {expediteur} traité : {sujet}")

def planifier_rendezvous():
    print("\n📅 PLANIFICATION DE RENDEZ-VOUS")
    print("-" * 30)
    titre = input("Titre du rendez-vous : ")
    date = input("Date (JJ/MM/AAAA) : ")
    heure = input("Heure (HH:MM) : ")
    print(f"\n✅ Rendez-vous '{titre}' planifié le {date} à {heure}")

def transcrire_note_vocale():
    print("\n🎤 TRANSCRIPTION DE NOTE VOCALE")
    print("-" * 30)
    print("Transcription simulée : 'Réunion importante demain à 10h'")

def afficher_statistiques():
    print("\n📊 STATISTIQUES")
    print("-" * 30)
    print("📧 Emails: 3")
    print("📅 Rendez-vous: 2")
    print("🎤 Notes vocales: 1")

def main():
    """Fonction principale avec boucle infinie"""
    while True:
        effacer_ecran()
        print("=" * 40)
        print("🤖 AGENT IA GRATUIT")
        print("=" * 40)
        print("1. Traiter un email")
        print("2. Planifier un rendez-vous")
        print("3. Transcrire une note vocale")
        print("4. Afficher les statistiques")
        print("0. 🚪 Quitter")
        print("=" * 40)
        
        choix = input("\nVotre choix (0-4) : ").strip()
        
        if choix == "1":
            traiter_email()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "2":
            planifier_rendezvous()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "3":
            transcrire_note_vocale()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "4":
            afficher_statistiques()
            input("\nAppuyez sur Entrée pour continuer...")
        elif choix == "0":
            print("\n👋 Au revoir !")
            break
        else:
            print("\n❌ Choix invalide ! Veuillez choisir entre 0 et 4.")
            input("Appuyez sur Entrée pour continuer...")

# Démarrer l'agent
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interruption - Au revoir !")
EOF
