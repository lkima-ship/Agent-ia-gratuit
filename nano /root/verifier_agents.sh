#!/bin/bash
echo "VERIFICATION DU SYSTEME D'AGENTS"
echo "================================="
echo ""
echo ""

# 1. Compter les agents
echo "1. STATISTIQUES :"
py_count=$(ls /root/*.py 2>/dev/null | wc -l)
agent_count=$(ls /root/agent_*.py 2>/dev/null | wc -l)
web_count=$(ls /root/*interface*.py 2>/dev/null | wc -l)
menu_count=$(ls /root/*menu*.py 2>/dev/null | wc -l)

echo "    • Fichiers Python : $py_count"
echo "    • Agents (agent_*) : $agent_count"
echo "    • Interfaces web : $web_count"
echo "    • Menus : $menu_count"
echo ""

# 2. Vérifier les exécutables
echo "2. ✓ AGENTS EXÉCUTABLES :"
count_exe=0
for file in /root/*.py; do
    if [ -x "$file" ]; then
        echo "    ✓ $(basename "$file")"
        count_exe=$((count_exe + 1))
    fi
done
echo "    Total exécutables : $count_exe"
echo ""

# 3. Agents principaux
echo "3. ✓ AGENTS PRINCIPAUX :"
important_agents=("menu_principal.py" "interface_agents_web.py" "hub_agents.py" "agent_ia_gratuit.py")

for agent in "${important_agents[@]}"; do
    if [ -f "/root/$agent" ]; then
        echo "    ✓ $agent (présent)"
    else
        echo "    ✗ $agent (manquant)"
    fi
done

# 4. Vérifier les ports utilisés
echo ""
echo "4. PORTS UTILISES :"
if command -v netstat &> /dev/null; then
    netstat -tulpn 2>/dev/null | grep -E ":80|:8080|:5000|:8000" || echo "    Aucun port web actif"
elif command -v ss &> /dev/null; then
    ss -tulpn 2>/dev/null | grep -E ":80|:8080|:5000|:8000" || echo "    Aucun port web actif"
else
    echo "    (netstat et ss non disponibles)"
fi

echo ""
echo "Vérification terminée."
