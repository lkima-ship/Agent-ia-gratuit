cat > /root/organize_agents.sh << 'EOF'
#!/bin/sh
echo "Organisation des agents..."
echo ""

# Création des dossiers
mkdir -p /root/agents_web /root/agents_ia /root/agents_system /root/agents_specialises

# Déplacement conditionnel
for agent in /root/agent_*.py; do
    name=$(basename "$agent")
    
    case "$name" in
        *web*)
            mv "$agent" /root/agents_web/ 2>/dev/null
            echo "Déplacé vers web: $name"
            ;;
        *ia*|*ai*|*ml*)
            mv "$agent" /root/agents_ia/ 2>/dev/null
            echo "Déplacé vers IA: $name"
            ;;
        *surveillance*|*moniteur*|*system*)
            mv "$agent" /root/agents_system/ 2>/dev/null
            echo "Déplacé vers system: $name"
            ;;
        *)
            mv "$agent" /root/agents_specialises/ 2>/dev/null
            echo "Déplacé vers spécialisés: $name"
            ;;
    esac
done

echo ""
echo "Organisation terminée !"
ls -d /root/agents_*/
EOF

chmod +x /root/organize_agents.sh
# Exécutez seulement si vous voulez réorganiser : sh /root/organize_agents.sh
