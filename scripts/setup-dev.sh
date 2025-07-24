#!/bin/bash

# Setup script for AI Career Discovery Assistant development environment

set -e

echo "🚀 Setting up AI Career Discovery Assistant development environment..."

# Check if running from project root
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Copy environment file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "📋 Copying environment template..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your GEMINI_API_KEY"
fi

# Install backend dependencies locally (for IDE support and migrations)
echo "🐍 Installing Python dependencies..."
cd backend
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD=python3.11
elif command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
else
    echo "❌ Error: Python 3 not found. Please install Python 3.11+"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
echo "🗄️  Running database migrations..."
# Start only the database service
cd ..
docker-compose up -d db
echo "Waiting for database to be ready..."
sleep 5

# Run migrations
cd backend
source venv/bin/activate
alembic upgrade head

cd ..

echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and add your GEMINI_API_KEY"
echo "2. Run 'make dev' or 'docker-compose up -d' to start all services"
echo "3. Access the application at http://localhost:3000"
echo "4. Access the API docs at http://localhost:8000/api/v1/docs"