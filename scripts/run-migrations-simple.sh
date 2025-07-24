#!/bin/bash

# Simple migration runner that bypasses complex configuration

set -e

echo "🗄️  Running database migrations (simplified)..."

# Start the database
docker-compose up -d db

# Wait for database
echo "Waiting for database..."
sleep 5

# Run migrations with minimal config
docker-compose run --rm \
  -e DATABASE_URL=postgresql://postgres:postgres@db:5432/career_assistant \
  backend \
  bash -c "mv alembic/env.py alembic/env_original.py && mv alembic/env_simple.py alembic/env.py && alembic upgrade head && mv alembic/env.py alembic/env_simple.py && mv alembic/env_original.py alembic/env.py"

echo "✅ Migrations completed successfully!"