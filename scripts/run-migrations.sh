#!/bin/bash

# Script to run database migrations

set -e

echo "🗄️  Running database migrations..."

# Method 1: Try using Docker Compose
if command -v docker-compose &> /dev/null; then
    echo "Using Docker Compose to run migrations..."
    
    # Ensure database is running
    docker-compose up -d db
    
    # Wait for database to be ready
    echo "Waiting for database to be ready..."
    sleep 5
    
    # Run migrations in a temporary container
    docker-compose run --rm backend alembic upgrade head
    
    echo "✅ Migrations completed successfully!"
    exit 0
fi

# Method 2: Fallback message
echo "❌ Docker Compose not found."
echo ""
echo "To run migrations manually:"
echo "1. Start the database: docker-compose up -d db"
echo "2. Install Python dependencies:"
echo "   cd backend"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install -r requirements.txt"
echo "3. Run migrations:"
echo "   alembic upgrade head"