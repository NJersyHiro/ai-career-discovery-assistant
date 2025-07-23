# AI Career Discovery Assistant - Makefile

.PHONY: help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development
.PHONY: dev
dev: ## Start development environment
	docker-compose up -d

.PHONY: dev-frontend
dev-frontend: ## Start frontend development server
	cd frontend && pnpm dev

.PHONY: dev-backend
dev-backend: ## Start backend development server
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: install
install: ## Install all dependencies
	cd frontend && pnpm install
	cd backend && pip install -e ".[dev]"

# Docker
.PHONY: build
build: ## Build Docker images
	docker-compose build

.PHONY: up
up: ## Start all services
	docker-compose up -d

.PHONY: down
down: ## Stop all services
	docker-compose down

.PHONY: logs
logs: ## View logs
	docker-compose logs -f

# Database
.PHONY: db-migrate
db-migrate: ## Run database migrations
	cd backend && alembic upgrade head

.PHONY: db-rollback
db-rollback: ## Rollback database migration
	cd backend && alembic downgrade -1

.PHONY: db-reset
db-reset: ## Reset database
	cd backend && alembic downgrade base && alembic upgrade head

# Testing
.PHONY: test
test: test-frontend test-backend ## Run all tests

.PHONY: test-frontend
test-frontend: ## Run frontend tests
	cd frontend && pnpm test

.PHONY: test-backend
test-backend: ## Run backend tests
	cd backend && pytest

.PHONY: test-e2e
test-e2e: ## Run E2E tests
	cd frontend && pnpm test:e2e

# Code Quality
.PHONY: lint
lint: lint-frontend lint-backend ## Run all linters

.PHONY: lint-frontend
lint-frontend: ## Lint frontend code
	cd frontend && pnpm lint

.PHONY: lint-backend
lint-backend: ## Lint backend code
	cd backend && ruff check . && mypy .

.PHONY: format
format: format-frontend format-backend ## Format all code

.PHONY: format-frontend
format-frontend: ## Format frontend code
	cd frontend && pnpm format

.PHONY: format-backend
format-backend: ## Format backend code
	cd backend && ruff format . && black .

# Security
.PHONY: security-check
security-check: ## Run security checks
	cd backend && pip-audit
	cd frontend && pnpm audit

# Clean
.PHONY: clean
clean: ## Clean build artifacts
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf frontend/dist frontend/build
	rm -rf backend/dist backend/build
	rm -rf .pytest_cache .coverage coverage.xml

.PHONY: clean-docker
clean-docker: ## Clean Docker resources
	docker-compose down -v
	docker system prune -f