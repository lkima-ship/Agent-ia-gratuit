cat > /root/check_system.sh << 'EOF'
#!/bin/bash
echo "=== VÉRIFICATION SYSTÈME ==="
echo ""
echo "Fichiers Python : $(find /root -maxdepth 1 -name "*.py" 2>/dev/null | wc -l)"
echo "Agents (agent_*.py) : $(find /root -maxdepth 1 -name "agent_*.py" 2>/dev/null | wc -l)"
echo ""
echo "Processus en cours :"
ps aux | grep -E "python|agent" | grep -v grep || echo "Aucun"
echo ""
echo "=== FIN ==="
EOF
