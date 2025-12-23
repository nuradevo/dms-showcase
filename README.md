# DMS Showcase — продвинутая версия (FastAPI + PostgreSQL + Alembic + JWT + Next.js)

Кратко:
- FastAPI backend с асинхронным SQLAlchemy, Alembic миграциями и JWT-аутентификацией.
- Next.js frontend (TypeScript) с логином, созданием и просмотром ICSR.
- Seed‑скрипт для создания demo‑пользователей и записей.
- Docker Compose для локального запуска.
- Devcontainer для Codespaces / VS Code.
- Скрипт для сборки ZIP (create_zip.sh).

Запуск (рекомендуемый — Docker):
1. Скопировать .env.example в backend/.env и frontend/.env.local и при необходимости отредактировать.
2. docker compose up --build
3. Backend: http://localhost:8000 (OpenAPI: /docs)
   Frontend: http://localhost:3000

Перед публикацией: убедитесь, что в репозитории нет реальных секретов или персональных данных.
