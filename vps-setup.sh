#!/bin/bash
set -e

# Catholic Ride Share - VPS Setup Script (Ubuntu 22.04)
# Run this on a fresh VPS to set up Docker and the application

echo "🚀 Catholic Ride Share - VPS Setup"
echo "=================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# Install Docker Compose plugin
echo "📦 Installing Docker Compose..."
sudo apt install -y docker-compose-plugin

# Create app directory
echo "📁 Creating application directory..."
sudo mkdir -p /opt/catholic-ride-share
sudo chown $USER:$USER /opt/catholic-ride-share
cd /opt/catholic-ride-share

echo ""
echo "✅ Docker installed successfully!"
echo ""
echo "⚠️  IMPORTANT: Log out and log back in for Docker permissions to take effect."
echo ""
echo "📋 Next steps:"
echo "   1. Log out and log back in (or run: newgrp docker)"
echo "   2. Copy these files to /opt/catholic-ride-share/:"
echo "      - docker-compose.prod.yml"
echo "      - nginx.conf"
echo "      - .env (copy from env.prod.template and edit)"
echo "   3. Run: cd /opt/catholic-ride-share"
echo "   4. Run: docker compose -f docker-compose.prod.yml pull"
echo "   5. Run: docker compose -f docker-compose.prod.yml up -d"
echo "   6. Run: docker compose -f docker-compose.prod.yml exec backend alembic upgrade head"
echo "   7. Run: docker compose -f docker-compose.prod.yml exec backend python -m app.seed_demo"
echo ""
echo "🌐 Your app will be available at http://YOUR_VPS_IP"
