cat > /root/agent_dashboard.sh << 'EOF'
#!/bin/sh
echo "=== TABLEAU DE BORD AGENTS ==="
echo ""
echo "📊 Python: $(ls /root/*.py 2>/dev/null | wc -l)"
echo "🚀 Agents: $(ls /root/agent_*.py 2>/dev/null | wc -l)"
echo "📋 Menus: $(ls /root/*menu*.py 2>/dev/null | wc -l)"
echo "🖥️ Interfaces: $(ls /root/*interface*.py 2>/dev/null | wc -l)"
echo ""
echo "✅ hub_agents.py: $([ -f "/root/hub_agents.py" ] && echo "PRÉSENT" || echo "ABSENT")"
echo "✅ menu_principal.py: $([ -f "/root/menu_principal.py" ] && echo "PRÉSENT" || echo "ABSENT")"
echo "✅ agent_web_avance.py: $([ -f "/root/agent_web_avance.py" ] && echo "PRÉSENT" || echo "ABSENT")"
echo ""
echo "=== $(date) ==="
EOF && chmod +x /root/agent_dashboard.sh && sh /root/agent_dashboard.sh
