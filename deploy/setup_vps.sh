#!/bin/bash

# Mise à jour du système
sudo apt update && sudo apt upgrade -y

# Installation Docker
sudo apt install -y docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker

# Installation Nginx (optionnel)
sudo apt install -y nginx certbot python3-certbot-nginx

# Cloner le projet
git clone https://github.com/votre-repo/agent-ia-gratuit.git
cd agent-ia-gratuit

# Configurer SSL avec Certbot
sudo certbot --nginx -d votre-domaine.com

# Lancer les services
docker-compose up -d

# Vérifier le statut
docker-compose ps
