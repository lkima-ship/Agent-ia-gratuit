cat > ~/simple_backup.py << 'EOF'
#!/usr/bin/env python3
"""
Système de backup simple pour projets Flask iPhone
"""
import os
import datetime
import tarfile
from pathlib import Path

def create_backup():
    """Crée une backup du projet Flask actuel"""
    project_path = input("Path to backup (default: current directory): ").strip()
    if not project_path:
        project_path = os.getcwd()
    
    if not os.path.exists(project_path):
        print(f"❌ Path not found: {project_path}")
        return
    
    project_name = os.path.basename(project_path.rstrip('/'))
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / "backups"
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f"{project_name}_{timestamp}.tar.gz"
    
    # Compresse le projet
    with tarfile.open(backup_file, 'w:gz') as tar:
        tar.add(project_path, arcname=project_name)
    
    size_kb = backup_file.stat().st_size / 1024
    print(f"✅ Backup created: {backup_file.name}")
    print(f"   Size: {size_kb:.1f} KB")
    print(f"   Location: {backup_dir}")

def list_backups():
    """Liste les backups disponibles"""
    backup_dir = Path.home() / "backups"
    
    if not backup_dir.exists():
        print("❌ No backups found")
        return
    
    backups = list(backup_dir.glob("*.tar.gz"))
    
    if not backups:
        print("❌ No backups found")
        return
    
    print("\n📦 Available backups:")
    for i, backup in enumerate(backups, 1):
        size_kb = backup.stat().st_size / 1024
        mod_time = datetime.datetime.fromtimestamp(backup.stat().st_mtime)
        print(f"{i}. {backup.name}")
        print(f"   Size: {size_kb:.1f} KB, Date: {mod_time.strftime('%Y-%m-%d %H:%M')}")

def restore_backup():
    """Restaure une backup"""
    backup_dir = Path.home() / "backups"
    
    if not backup_dir.exists():
        print("❌ No backups found")
        return
    
    backups = list(backup_dir.glob("*.tar.gz"))
    
    if not backups:
        print("❌ No backups found")
        return
    
    print("\n📦 Available backups:")
    for i, backup in enumerate(backups, 1):
        print(f"{i}. {backup.name}")
    
    try:
        choice = int(input("\nSelect backup number: ").strip())
        if 1 <= choice <= len(backups):
            selected = backups[choice - 1]
            restore_path = input(f"Restore to path (default: current directory): ").strip()
            if not restore_path:
                restore_path = os.getcwd()
            
            if not os.path.exists(restore_path):
                print(f"❌ Restore path does not exist: {restore_path}")
                return
            
            with tarfile.open(selected, 'r:gz') as tar:
                tar.extractall(restore_path)
            
            print(f"✅ Backup restored to: {restore_path}")
        else:
            print("❌ Invalid choice")
    except ValueError:
        print("❌ Please enter a number")

def main():
    """Menu principal"""
    while True:
        print("\n💾 Simple Backup System")
        print("=" * 40)
        print("1. Create backup")
        print("2. List backups")
        print("3. Restore backup")
        print("4. Exit")
        
        choice = input("\nChoice (1-4): ").strip()
        
        if choice == '1':
            create_backup()
        elif choice == '2':
            list_backups()
        elif choice == '3':
            restore_backup()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")

if __name__ == '__main__':
    main()
EOF
