# RCM GCC Platform Makefile

.PHONY: help up down build logs seed clean test

# Default target
help:
	@echo "RCM GCC Platform - Available Commands:"
	@echo ""
	@echo "  make up      - Start all services (build if needed)"
	@echo "  make down    - Stop all services"
	@echo "  make build   - Build all Docker images"
	@echo "  make logs     - Show logs from all services"
	@echo "  make seed     - Seed database with demo data"
	@echo "  make clean    - Remove all containers and volumes"
	@echo "  make test     - Run tests"
	@echo ""

# Start all services
up:
	@echo "Starting RCM GCC Platform..."
	docker-compose -f infra/docker-compose.yml up --build -d
	@echo "Services started! Access at:"
	@echo "  Frontend: http://localhost:3001"
	@echo "  API: http://localhost:8000"
	@echo "  Database: localhost:5432"

# Stop all services
down:
	@echo "Stopping RCM GCC Platform..."
	docker-compose -f infra/docker-compose.yml down
	@echo "Services stopped!"

# Build all images
build:
	@echo "Building Docker images..."
	docker-compose -f infra/docker-compose.yml build
	@echo "Build complete!"

# Show logs
logs:
	@echo "Showing logs from all services..."
	docker-compose -f infra/docker-compose.yml logs -f

# Seed database
seed:
	@echo "Seeding database with demo data..."
	docker-compose -f infra/docker-compose.yml exec api python -m app.rcm.seed
	@echo "Database seeded successfully!"

# Clean everything
clean:
	@echo "Cleaning up containers and volumes..."
	docker-compose -f infra/docker-compose.yml down -v --remove-orphans
	docker system prune -f
	@echo "Cleanup complete!"

# Run tests
test:
	@echo "Running tests..."
	@echo "API tests:"
	cd api && uv run pytest
	@echo "Frontend tests:"
	cd web && yarn test
	@echo "Tests complete!"

# Development helpers
dev-api:
	@echo "Starting API in development mode..."
	cd api && uv run dev

dev-web:
	@echo "Starting frontend in development mode..."
	cd web && yarn dev

# Health check
health:
	@echo "Checking service health..."
	@echo "API Health:"
	curl -f http://localhost:8000/health || echo "API not responding"
	@echo "Frontend Health:"
	curl -f http://localhost:3001 || echo "Frontend not responding"
	@echo "Database Health:"
	docker-compose -f infra/docker-compose.yml exec db pg_isready -U postgres || echo "Database not responding"
