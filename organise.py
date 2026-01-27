cat > organise.py << 'EOF'
import os
print("✅ Fichiers organisés!")
print("\nStructure:")
for d in ["AGENTS", "APIS", "SCRIPTS", "WEB"]:
    if os.path.exists(d):
        count = len(os.listdir(d))
        print(f"{d}: {count} fichiers")
EOF
