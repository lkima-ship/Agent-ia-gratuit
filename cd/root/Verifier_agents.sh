#!/bin/bash
echo "VERIFICATION DU SYSTEME D'AGENTS"
echo "=============================="
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
for file in /root/*.py; do
    if [ -x "$file" ]; then
        echo "    ✓ $(basename "$file")"
    fi
done  # <-- CECI ÉTAIT MANQUANT !

# 3. Vérifier les agents en cours d'exécution
echo ""
echo "3. AGENTS ACTIFS :"
ps aux | grep -E "python.*agent|python.*menu|python.*interface" | grep -v grep

# 4. Vérifier les ports utilisés
echo ""
echo "4. PORTS UTILISES :"
netstat -tulpn 2>/dev/null | grep -E ":80|:8080|:5000|:8000" || echo "    (commande netstat non disponible)"

echo ""
echo "Vérification terminée."
