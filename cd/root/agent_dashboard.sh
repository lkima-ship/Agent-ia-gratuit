cat > /root/agent_dashboard.sh << 'EOF'
#!/bin/sh
echo "========================================"
echo "   TABLEAU DE BORD AGENTS IA"
echo "========================================"
echo ""

# Statistiques
echo "📊 STATISTIQUES :"
echo "   Fichiers Python: $(ls /root/*.py 2>/dev/null | wc -l)"
echo "   Agents: $(ls /root/agent_*.py 2>/dev/null | wc -l)"
echo "   Menus: $(ls /root/*menu*.py 2>/dev/null | wc -l)"
echo "   Interfaces: $(ls /root/*interface*.py 2>/dev/null | wc -l)"
echo ""

# Top agents
echo "🎯 TOP 10 AGENTS :"
count=1
for agent in /root/agent_*.py; do
    [ $count -gt 10 ] && break
    if [ -f "$agent" ]; then
        echo "   $count. $(basename $agent)"
        count=$((count + 1))
    fi
done
echo ""

# État
echo "🔍 ÉTAT :"
[ -f "/root/hub_agents.py" ] && echo "   ✅ hub_agents.py" || echo "   ❌ hub_agents.py"
[ -f "/root/menu_principal.py" ] && echo "   ✅ menu_principal.py" || echo "   ❌ menu_principal.py"
[ -f "/root/agent_web_avance.py" ] && echo "   ✅ agent_web_avance.py" || echo "   ❌ agent_web_avance.py"
echo ""

echo "========================================"
echo "   $(date)"
echo "========================================"
EOF

chmod +x /root/agent_dashboard.sh
