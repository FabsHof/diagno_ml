.PHONY: help install lint format test build up down logs clean demo

# Default target
help:
	@echo "DiagnoML Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  install     Install dependencies with uv"
	@echo "  setup       Full setup (install + pre-commit)"
	@echo ""
	@echo "Development:"
	@echo "  lint        Run linter (ruff)"
	@echo "  format      Format code (ruff)"
	@echo "  typecheck   Run type checker (mypy)"
	@echo "  test        Run all tests"
	@echo "  test-unit   Run unit tests only"
	@echo "  test-int    Run integration tests"
	@echo ""
	@echo "Docker:"
	@echo "  build       Build Docker images"
	@echo "  up          Start all services"
	@echo "  down        Stop all services"
	@echo "  logs        Follow container logs"
	@echo "  clean       Stop and remove volumes"
	@echo ""
	@echo "Demo:"
	@echo "  demo        Run demo workflow"
	@echo "  seed        Seed synthetic data"

# Setup
install:
	uv sync

setup: install
	uv run pre-commit install
	cp .env.example .env

# Development
lint:
	uv run ruff check .

format:
	uv run ruff format .
	uv run ruff check --fix .

typecheck:
	uv run mypy src/

test:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

test-unit:
	uv run pytest tests/unit -v -m unit

test-int:
	uv run pytest tests/integration -v -m integration

# Docker
build:
	DOCKER_BUILDKIT=1 docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

clean:
	docker compose down -v
	docker system prune -f

# Demo
demo:
	uv run python scripts/run_demo.py

seed:
	uv run python scripts/seed_data.py