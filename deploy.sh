#!/bin/bash

# AI Career Discovery Assistant - Deployment Script
# This script helps deploy the application to production

set -e

echo "🚀 AI Career Discovery Assistant - Deployment Script"
echo "=================================================="

# Check if .env.production exists
if [ ! -f .env.production ]; then
    echo "❌ Error: .env.production file not found!"
    echo "Please copy .env.production.example to .env.production and configure it."
    exit 1
fi

# Load environment variables
export $(cat .env.production | grep -v '^#' | xargs)

# Function to generate secure random strings
generate_secret() {
    openssl rand -base64 32
}

# Check if required variables are set
if [ -z "$GEMINI_API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY is not set in .env.production"
    exit 1
fi

if [ -z "$SECRET_KEY" ] || [ "$SECRET_KEY" = "your-very-long-random-secret-key-at-least-32-characters" ]; then
    echo "⚠️  Generating new SECRET_KEY..."
    NEW_SECRET=$(generate_secret)
    sed -i "s/SECRET_KEY=.*/SECRET_KEY=$NEW_SECRET/" .env.production
    echo "✅ SECRET_KEY generated and saved"
fi

if [ -z "$JWT_SECRET_KEY" ] || [ "$JWT_SECRET_KEY" = "another-very-long-random-jwt-secret-key" ]; then
    echo "⚠️  Generating new JWT_SECRET_KEY..."
    NEW_JWT_SECRET=$(generate_secret)
    sed -i "s/JWT_SECRET_KEY=.*/JWT_SECRET_KEY=$NEW_JWT_SECRET/" .env.production
    echo "✅ JWT_SECRET_KEY generated and saved"
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p nginx/ssl
mkdir -p backups

# Pull latest changes
echo "📥 Pulling latest changes from git..."
git pull origin main

# Build and start services
echo "🏗️  Building Docker images..."
docker compose -f docker-compose.prod.yml build

echo "🚀 Starting services..."
docker compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Create S3 bucket in MinIO
echo "🪣 Creating S3 bucket in MinIO..."
docker compose -f docker-compose.prod.yml exec -T minio mc alias set myminio http://localhost:9000 $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY || true
docker compose -f docker-compose.prod.yml exec -T minio mc mb myminio/$S3_BUCKET_NAME || true
docker compose -f docker-compose.prod.yml exec -T minio mc anonymous set public myminio/$S3_BUCKET_NAME || true

# Check service health
echo "🏥 Checking service health..."
docker compose -f docker-compose.prod.yml ps

# Show logs
echo "📋 Recent logs:"
docker compose -f docker-compose.prod.yml logs --tail=20

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📌 Next steps:"
echo "1. Set up SSL certificates (see DEPLOYMENT.md)"
echo "2. Configure your domain to point to this server"
echo "3. Set up monitoring and backups"
echo "4. Test the application at http://your-server-ip"
echo ""
echo "📖 For more information, see DEPLOYMENT.md"