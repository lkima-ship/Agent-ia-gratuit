# 1. Supprimer le fichier corrompu
rm -f /root/verifier_agents.sh

# 2. Créer un script propre et simple
cat > /root/verifier_agents.sh << 'EOF'
#!/bin/bash

clear
echo "========================================="
echo "  VÉRIFICATION DU SYSTÈME D'AGENTS IA   "
echo "========================================="
echo ""

# 1. COMPTER LES FICHIERS
echo "1. 📊 STATISTIQUES :"
py_count=$(find /root -maxdepth 1 -name "*.py" -type f 2>/dev/null | wc -l)
agent_count=$(find /root -maxdepth 1 -name "agent_*.py" -type f 2>/dev/null | wc -l)
web_count=$(find /root -maxdepth 1 -name "*interface*.py" -type f 2>/dev/null | wc -l)
menu_count=$(find /root -maxdepth 1 -name "*menu*.py" -type f 2>/dev/null | wc -l)

echo "   • Fichiers Python : $py_count"
echo "   • Agents (agent_*) : $agent_count"
echo "   • Interfaces web : $web_count"
echo "   • Menus : $menu_count"
echo ""

# 2. VÉRIFIER LES EXÉCUTABLES
echo "2. ✅ AGENTS EXÉCUTABLES :"
count_exe=0
for file in /root/*.py; do
    if [[ -f "$file" && -x "$file" ]]; then
        echo "   ✅ $(basename "$file")"
        count_exe=$((count_exe + 1))
    fi
done
echo "   Total exécutables : $count_exe"
echo ""

# 3. AGENTS IMPORTANTS
echo "3. 🎯 AGENTS PRINCIPAUX :"
declare -a important_agents=(
    "menu_principal.py"
    "interface_agents_web.py" 
    "hub_agents.py"
    "agent_ia_gratuit.py"
    "agent_web_avance.py"
    "dashboard_web_agent.py"
)

for agent in "${important_agents[@]}"; do
    if [[ -f "/root/$agent" ]]; then
        echo "   ✅ $agent"
    else
        echo "   ❌ $agent (absent)"
    fi
done
echo ""

# 4. PROCESSUS EN COURS
echo "4. 🔄 AGENTS ACTIFS :"
active_agents=$(ps aux | grep -E "python.*(agent|menu|interface|dashboard)" | grep -v grep)
if [[ -n "$active_agents" ]]; then
    echo "$active_agents" | while IFS= read -r line; do
        echo "   📌 $line"
    done
else
    echo "   Aucun agent actif"
fi
echo ""

# 5. PORTS OUVERTS
echo "5. 🌐 PORTS UTILISÉS :"
if command -v ss >/dev/null 2>&1; then
    ss -tulpn 2>/dev/null | grep -E ":80|:8080|:5000|:8000" || echo "   Aucun port web détecté"
elif command -v netstat >/dev/null 2>&1; then
    netstat -tulpn 2>/dev/null | grep -E ":80|:8080|:5000|:8000" || echo "   Aucun port web détecté"
else
    echo "   Impossible de vérifier les ports"
fi

echo ""
echo "========================================="
echo "     VÉRIFICATION TERMINÉE ✓"
echo "========================================="
EOF

# 3. Rendre exécutable
chmod +x /root/verifier_agents.sh

# 4. Tester
bash -n /root/verifier_agents.sh && echo "✅ Syntaxe OK" || echo "❌ Erreur de syntaxe"
echo ""
bash /root/verifier_agents.sh
