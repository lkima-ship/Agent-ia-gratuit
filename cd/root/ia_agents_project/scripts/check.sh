cat > ai_agents_project/scripts/check.sh << 'EOF'
#!/bin/sh

echo "🔍 Vérification du système..."

# 1. Structure
echo "1. Structure des dossiers:"
find /root/ai_agents_project -type d | sort

# 2. Fichiers
echo -e "\n2. Fichiers créés:"
find /root/ai_agents_project -type f | sort

# 3. Python
echo -e "\n3. Environnement Python:"
python3 --version
pip3 list 2>/dev/null | grep flask || echo "Flask non installé"

# 4. Port 5002
echo -e "\n4. Port 5002:"
netstat -tulpn 2>/dev/null | grep :5002 || \
    ss -tulpn 2>/dev/null | grep :5002 || \
    echo "Port non occupé"

# 5. Processus
echo -e "\n5. Processus API:"
ps aux | grep -E "python.*main|:5002" | grep -v grep || echo "Aucun processus"
EOF

chmod +x ai_agents_project/scripts/check.sh
