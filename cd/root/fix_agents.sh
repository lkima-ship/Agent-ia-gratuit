# Créer un script ash-compatible
cat > /root/fix_agents.sh << 'EOF'
#!/bin/sh
# Script ash-compatible pour Alpine Linux

echo "🔧 CORRECTION DES AGENTS IA - ALPINE"
echo "====================================="
echo ""

# Vérifier le shell
echo "Shell: $SHELL"
echo "Répertoire: $(pwd)"
echo ""

# Liste des fichiers attendus
echo "📁 FICHIERS ATTENDUS :"
expected_files="web_interface.py agent_cognitif.py agent_ia_ml.py plugin_manager.py"
missing=0

for file in $expected_files; do
    if [ -f "/root/$file" ]; then
        size=$(wc -c < "/root/$file" 2>/dev/null || echo "0")
        if [ "$size" -gt 10 ]; then
            echo "✅ $file ($size octets)"
            chmod 755 "/root/$file" 2>/dev/null
        else
            echo "⚠️  $file (vide ou presque: $size octets)"
            missing=1
        fi
    else
        echo "❌ $file (manquant)"
        missing=1
    fi
done

echo ""

# Réparer si nécessaire
if [ "$missing" -eq 1 ]; then
    echo "🛠️  RÉPARATION AUTOMATIQUE..."
    
    # Recréer web_interface.py
    if [ ! -f "/root/web_interface.py" ] || [ $(wc -c < "/root/web_interface.py" 2>/dev/null || echo "0") -lt 10 ]; then
        echo "Création de web_interface.py..."
        cat > /root/web_interface.py << 'PYEOF'
print("Interface Web Agents IA")
print("Version minimale Alpine")
PYEOF
    fi
    
    # Recréer agent_cognitif.py
    if [ ! -f "/root/agent_cognitif.py" ] || [ $(wc -c < "/root/agent_cognitif.py" 2>/dev/null || echo "0") -lt 10 ]; then
        echo "Création de agent_cognitif.py..."
        cat > /root/agent_cognitif.py << 'PYEOF'
print("Agent Cognitif")
print("Version minimale Alpine")
PYEOF
    fi
    
    # Rendre exécutable
    chmod +x /root/*.py 2>/dev/null
    echo "✅ Réparation terminée"
fi

echo ""
echo "🚀 TESTS :"
echo "1. Test Python:"
python3 --version
echo ""
echo "2. Test des fichiers:"
for file in web_interface.py agent_cognitif.py; do
    if [ -f "/root/$file" ]; then
        echo "Test de $file:"
        python3 "/root/$file" --help 2>&1 | head -2 || echo "  Erreur d'exécution"
    fi
done

echo ""
echo "📡 POUR LANCER:"
echo "  python3 /root/web_interface.py"
echo "  python3 /root/agent_cognitif.py"
EOF

# Exécuter le script
chmod +x /root/fix_agents.sh
/root/fix_agents.sh
