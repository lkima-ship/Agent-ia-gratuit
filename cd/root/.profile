# Ajouter ces alias à ~/.profile
cat >> ~/.profile << 'EOF'

# Commandes API Flask
alias api-start="cd /root && nohup python3 simple_working.py > /tmp/api.log 2>&1 & echo \$! > /tmp/api.pid"
alias api-stop="pkill -f python 2>/dev/null; rm -f /tmp/api.pid"
alias api-status="if ps aux | grep -v grep | grep 'simple_working.py' >/dev/null; then echo 'API en cours'; else echo 'API arrêtée'; fi"
alias api-test="curl -s http://localhost:5002 && echo ''"
alias api-logs="tail -f /tmp/api.log"

EOF

# Charger
source ~/.profile
