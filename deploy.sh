#!/bin/bash
set -e

# Catholic Ride Share - Build and Push Script
# Usage: ./deploy.sh [tag]
# Example: ./deploy.sh v1.0.0

TAG="${1:-latest}"
DOCKER_USERNAME="${DOCKER_USERNAME:?Set DOCKER_USERNAME environment variable}"

echo "🏗️  Building and pushing images with tag: $TAG"

# Build and push backend
echo ""
echo "📦 Building backend..."
docker build -t "$DOCKER_USERNAME/catholic-ride-share-backend:$TAG" ./backend
docker push "$DOCKER_USERNAME/catholic-ride-share-backend:$TAG"
echo "✅ Backend pushed!"

# Build and push frontend
echo ""
echo "📦 Building frontend..."
docker build -t "$DOCKER_USERNAME/catholic-ride-share-frontend:$TAG" ./frontend
docker push "$DOCKER_USERNAME/catholic-ride-share-frontend:$TAG"
echo "✅ Frontend pushed!"

echo ""
echo "🎉 Done! Images pushed to Docker Hub:"
echo "   - $DOCKER_USERNAME/catholic-ride-share-backend:$TAG"
echo "   - $DOCKER_USERNAME/catholic-ride-share-frontend:$TAG"
echo ""
echo "📋 Next steps on your VPS:"
echo "   1. Copy docker-compose.prod.yml, nginx.conf, and .env to your VPS"
echo "   2. Edit .env with your settings"
echo "   3. Run: docker compose -f docker-compose.prod.yml pull"
echo "   4. Run: docker compose -f docker-compose.prod.yml up -d"
echo "   5. Run migrations: docker compose -f docker-compose.prod.yml exec backend alembic upgrade head"
echo "   6. Seed demo data: docker compose -f docker-compose.prod.yml exec backend python -m app.seed_demo"
