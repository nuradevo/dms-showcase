DMS Showcase — продвинутая демонстрация (микро‑демо)

Кратко
Это демонстрационный репозиторий (мини‑версия корпоративной DMS) с минимальной полной стековой реализацией:
- Backend: FastAPI + async SQLAlchemy (Postgres для docker-compose; fallback — sqlite)
- Alembic миграции (папка backend/alembic)
- JWT‑аутентификация (token endpoint)
- Seed‑скрипты для создания demo‑пользователей и записей
- Frontend: Next.js (TypeScript) — страницы логина и списка/создания ICSR
- ML endpoint: простая NER inference (spaCy или mock)
- Docker Compose + devcontainer для быстрого старта
- CI: GitHub Actions (lint / тесты) — шаблон включён
- pre-commit config для форматирования/линтинга

Что включено в репо
- backend/ — FastAPI приложение и миграции
- frontend/ — minimal Next.js demo (pages, стили)
- docker-compose.yml — поднятие Postgres, Redis, backend, frontend
- .devcontainer/ — ускоренный запуск в Codespaces / VS Code
- скрипты seed_demo для заполнения тестовыми данными

Быстрый старт (рекомендуется: Docker)
1) Клонировать:
   git clone https://github.com/<ваш-пользователь>/dms-showcase.git
   cd dms-showcase

2) Скопировать примеры env:
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local

3) Поднять сервисы:
   docker compose up --build

4) Инициализировать миграции (опционально, если вы не используете встроённый запуск):
   docker compose exec backend alembic -c backend/alembic.ini upgrade head

5) Сеединг демо‑данных:
   docker compose exec backend python -m app.seed_demo

6) Открыть:
   Frontend: http://localhost:3000  
   Backend OpenAPI: http://localhost:8000/docs

Demo‑учётные данные (seed)
- admin: admin@demo / Admin123!
- user: user@demo / User123!

Что демонстрируется
- full‑stack интеграция: frontend ↔ backend ↔ DB
- простая ML‑инференция через /ml/ner (spaCy fallback)
- JWT‑auth flow и защита endpoint'ов
- alembic миграции и seed скрипт для воспроизводимой среды
- devcontainer / Codespaces support

Что НЕ публикуется
- реальные персональные данные (PHI/PII)
- реальные секреты (JWT_SECRET, AWS ключи и т.д.)
- проприетарные / NDA‑данные

Рекомендации перед публикацией
- смените JWT_SECRET в backend/.env и не коммитьте реальные значения
- проверьте git history на утечки секретов перед публичным открытием:
  git grep -n "SECRET\|PASSWORD\|TOKEN\|AWS\|GCP"

Дальше (рекомендуемые улучшения)
- добавить unit и integration тесты (pytest) для основных flow
- добавить E2E (Cypress) для ключевых сценариев UI
- добавить badges (build/tests) и скриншот/GIF в README
- настроить автоматический запуск миграций в entrypoint контейнера (если нужно)

Контакты
Анастасия Федина — byby10240@gmail.com — Москва, Россия
