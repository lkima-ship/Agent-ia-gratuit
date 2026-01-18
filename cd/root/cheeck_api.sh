cat > /root/check_api.sh << 'EOF'
#!/bin/sh
echo "🔍 Vérification API..."

# Test 1: Processus
echo "1. Processus Python:"
ps aux | grep -E "python.*:5002|flask" | grep -v grep || echo "  Aucun"

# Test 2: Port
echo -e "\n2. Port 5002:"
if command -v ss >/dev/null; then
    ss -tulpn | grep :5002 || echo "  Port fermé"
else
    echo "  Installer ss: apk add iproute2"
fi

# Test 3: Curl
echo -e "\n3. Test HTTP:"
timeout 3 curl -s http://localhost:5002/api/status > /tmp/test_api.txt
if [ $? -eq 0 ]; then
    echo "  ✅ API accessible"
    cat /tmp/test_api.txt
else
    echo "  ❌ API non accessible"
fi

# Test 4: Fichiers
echo -e "\n4. Fichiers agents:"
ls /root/*.py | grep -i agent | head -5
EOF

chmod +x /root/check_api.sh
