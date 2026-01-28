#!/usr/bin/env python3
"""
SMART ORGANIZE - Organisateur intelligent de fichiers
Version complète avec catégories et confirmation
"""

import os
import shutil
import time
from pathlib import Path

# Configuration des catégories
CATEGORIES = {
    "Menus": ["menu", "dashboard"],
    "Interfaces": ["dashboard", "interface", "ui", "web"],
    "Agents": ["agent", "assistant", "bot"],
    "API": ["api", "rest", "endpoint"],
    "Scripts": ["script", "util", "tool"],
    "Moniteurs": ["moniteur", "monitor", "surveillance"],
    "Sites Web": ["html", "htm", "web", "site"],
    "Organiseurs": ["organise", "organize", "arrange", "trier"],
    "Autres": []  # Fichiers non classés
}

def clear_screen():
    """Efface l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête du programme"""
    print("=" * 60)
    print("🤖 ORGANISATEUR INTELLIGENT")
    print("=" * 60)
    print()

def categorize_file(filename):
    """Détermine la catégorie d'un fichier"""
    filename_lower = filename.lower()
    
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in filename_lower:
                return category
    
    return "Autres"

def analyze_files(directory="."):
    """Analyse les fichiers et les regroupe par catégorie"""
    files_by_category = {category: [] for category in CATEGORIES.keys()}
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        # Ignorer les dossiers et les fichiers cachés
        if os.path.isfile(item_path) and not item.startswith('.'):
            category = categorize_file(item)
            files_by_category[category].append(item)
    
    # Retirer les catégories vides
    return {k: v for k, v in files_by_category.items() if v}

def display_analysis(results):
    """Affiche les résultats de l'analyse"""
    total_files = sum(len(files) for files in results.values())
    
    print(f"📊 Analyse terminée: {total_files} fichiers trouvés\n")
    
    for category, files in sorted(results.items()):
        if files:  # Afficher seulement les catégories avec des fichiers
            print(f"📂 {category} ({len(files)} fichiers):")
            for file in sorted(files):
                print(f"  - {file}")
            print()
    
    print(f"⏱️  Total: {total_files} fichiers à organiser")
    print("-" * 40)

def organize_files(results, directory="."):
    """Organise les fichiers dans des sous-dossiers"""
    total_moved = 0
    
    for category, files in results.items():
        # Créer le dossier de catégorie s'il n'existe pas
        category_dir = os.path.join(directory, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Déplacer les fichiers
        for file in files:
            src = os.path.join(directory, file)
            dst = os.path.join(category_dir, file)
            
            try:
                shutil.move(src, dst)
                print(f"✅ {file} → {category}/")
                total_moved += 1
            except Exception as e:
                print(f"❌ Erreur avec {file}: {e}")
    
    return total_moved

def create_structure():
    """Crée la structure de dossiers recommandée"""
    directories = [
        "Agents IA",
        "APIs", 
        "Scripts",
        "Sites Web",
        "Moniteurs",
        "Organiseurs",
        "Interfaces",
        "Menus"
    ]
    
    print("🏗️  Création de la structure de dossiers...")
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Créé: {directory}/")
    
    print("\n✅ Structure créée avec succès!")

def organize_by_extension(directory="."):
    """Organise les fichiers par extension"""
    extensions_found = {}
    
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        
        if os.path.isfile(item_path) and not item.startswith('.'):
            # Obtenir l'extension
            ext = os.path.splitext(item)[1].lower()
            if ext:
                ext = ext[1:]  # Retirer le point
            else:
                ext = "sans_extension"
            
            # Créer le dossier d'extension
            ext_dir = os.path.join(directory, f"Ext_{ext.upper()}")
            os.makedirs(ext_dir, exist_ok=True)
            
            # Déplacer le fichier
            try:
                shutil.move(item_path, os.path.join(ext_dir, item))
                if ext not in extensions_found:
                    extensions_found[ext] = 0
                extensions_found[ext] += 1
                print(f"✅ {item} → Ext_{ext.upper()}/")
            except Exception as e:
                print(f"❌ Erreur avec {item}: {e}")
    
    print(f"\n📊 Organisé {sum(extensions_found.values())} fichiers par extension")

def interactive_mode():
    """Mode interactif avec confirmation"""
    print_header()
    
    # Analyse initiale
    print("🔍 Analyse des fichiers en cours...\n")
    time.sleep(1)
    
    results = analyze_files()
    
    if not results:
        print("❌ Aucun fichier à organiser.")
        input("\n↪ Appuyez sur Entrée pour continuer...")
        return
    
    # Affichage des résultats
    display_analysis(results)
    
    # Demander confirmation
    while True:
        choice = input("\n❓ Exécuter l'organisation ? (oui/non): ").strip().lower()
        
        if choice in ['oui', 'o', 'yes', 'y']:
            print("\n🔗 Organisation en cours...\n")
            total_moved = organize_files(results)
            print(f"\n✅ Organisation terminée ! ({total_moved} fichiers déplacés)")
            break
        elif choice in ['non', 'n', 'no']:
            print("\n⏹️  Organisation annulée.")
            break
        else:
            print("❌ Veuillez répondre par 'oui' ou 'non'")
    
    input("\n↪ Appuyez sur Entrée pour continuer...")

def quick_organize():
    """Organisation rapide sans confirmation"""
    print("⚡ Organisation rapide en cours...\n")
    
    results = analyze_files()
    
    if results:
        total_moved = organize_files(results)
        print(f"\n✅ {total_moved} fichiers organisés automatiquement!")
    else:
        print("❌ Aucun fichier à organiser.")
    
    time.sleep(2)

def main_menu():
    """Menu principal de l'organisateur"""
    while True:
        clear_screen()
        print_header()
        
        print("📋 MENU PRINCIPAL:")
        print("1. 🎯 Organiser les fichiers intelligemment (mode interactif)")
        print("2. ⚡ Organiser rapidement (sans confirmation)")
        print("3. 📁 Organiser par extension de fichier")
        print("4. 🏗️  Créer la structure de dossiers recommandée")
        print("5. 🔍 Analyser les fichiers sans organiser")
        print("6. ❌ Quitter")
        print("\n" + "-" * 40)
        
        choice = input("\nVotre choix (1-6): ").strip()
        
        if choice == "1":
            interactive_mode()
        elif choice == "2":
            quick_organize()
        elif choice == "3":
            organize_by_extension()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "4":
            create_structure()
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "5":
            print_header()
            results = analyze_files()
            display_analysis(results)
            input("\n↪ Appuyez sur Entrée pour continuer...")
        elif choice == "6":
            print("\n👋 Au revoir !")
            time.sleep(1)
            break
        else:
            print("\n❌ Choix invalide !")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n⏹️  Organisation interrompue.")
        time.sleep(1)
