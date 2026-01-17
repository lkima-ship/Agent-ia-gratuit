cat > /root/agent_dashboard.sh << 'EOF'
#!/bin/sh
echo "========================================"
echo "   TABLEAU DE BORD AGENTS IA"
echo "========================================"
echo ""

# 1. STATISTIQUES DÉTAILLÉES
echo "📊 STATISTIQUES COMPLÈTES :"
echo "   Fichiers Python: $(ls /root/*.py 2>/dev/null | wc -l)"
echo "   Agents: $(ls /root/agent_*.py 2>/dev/null | wc -l)"
echo "   Menus: $(ls /root/*menu*.py 2>/dev/null | wc -l)"
echo "   Interfaces: $(ls /root/*interface*.py 2>/dev/null | wc -l)"
echo "   Dashboards: $(ls /root/*dashboard*.py 2>/dev/null | wc -l)"
echo "   APIs: $(ls /root/*api*.py 2>/dev/null | wc -l)"
echo ""

# 2. AGENTS PAR CATÉGORIE
echo "🎯 AGENTS PAR CATÉGORIE :"
for agent in /root/agent_*.py; do
    if [ -f "$agent" ]; then
        name=$(basename "$agent" .py)
        echo "   • $name"
    fi
done | head -20
echo "   ... (total: $(ls /root/agent_*.py 2>/dev/null | wc -l))"
echo ""

# 3. ÉTAT DES AGENTS IMPORTANTS
echo "🔍 ÉTAT DES AGENTS CLÉS :"
check_agent() {
    if [ -f "/root/$1" ]; then
        echo "   ✅ $1"
        return 0
    else
        echo "   ❌ $1 (manquant)"
        return 1
    fi
}

check_agent "hub_agents.py"
check_agent "menu_principal.py"
check_agent "agent_ia_gratuit.py"
check_agent "agent_web_avance.py"
check_agent "dashboard_web_agent.py"
check_agent "interface_agents_web.py"
echo ""

# 4. SYSTÈME
echo "⚙️  SYSTÈME :"
echo "   CPU: $(grep -c ^processor /proc/cpuinfo) cores"
echo "   RAM: $(free -m | awk 'NR==2{printf "%.1f/%.0fMB (%.1f%%)", $3,$2,$3*100/$2}')"
echo "   Disk: $(df -h / | awk 'NR==2{print $3 "/" $2 " (" $5 ")"}')"
echo ""

# 5. RECOMMANDATIONS
echo "💡 RECOMMANDATIONS :"
if [ ! -f "/root/menu_principal.py" ]; then
    echo "   1. Créer un menu_principal.py pour centraliser l'accès"
fi
if [ ! -f "/root/agent_ia_gratuit.py" ]; then
    echo "   2. Recréer agent_ia_gratuit.py (agent principal)"
fi
if [ $(ls /root/agent_*.py 2>/dev/null | wc -l) -gt 15 ]; then
    echo "   3. Organiser les 15+ agents dans des sous-dossiers"
fi
echo ""

echo "========================================"
echo "   $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
EOF

chmod +x /root/agent_dashboard.sh
sh /root/agent_dashboard.sh
