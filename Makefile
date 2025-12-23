.PHONY: help up build down seed migrate test lint

help:
	@echo "Makefile commands:"
	@echo "  make up         - docker compose up --build"
	@echo "  make down       - docker compose down"
	@echo "  make seed       - run seed script in backend container"
	@echo "  make migrate    - run alembic upgrade head"
	@echo "  make test       - run backend pytest"
	@echo "  make lint       - run ruff / black locally (if installed)"

up:
	docker compose up --build

down:
	docker compose down

seed:
	docker compose exec backend python -m app.seed_demo

migrate:
	docker compose exec backend alembic -c backend/alembic.ini upgrade head

test:
	cd backend && pytest -q

lint:
	@echo "Run black/ruff locally (ensure pre-commit is set up)"
	ruff .
	black .
