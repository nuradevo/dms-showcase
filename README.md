# DMS Showcase — Demo for resume / interview

[![CI](https://github.com/nuradevo/dms-showcase/actions/workflows/ci.yml/badge.svg)](https://github.com/nuradevo/dms-showcase/actions/workflows/ci.yml)

Demo repository for the Document Management System (DMS) sample with mock data.

What this demo shows
- FastAPI backend (async SQLAlchemy) with JWT auth, Alembic migrations and seed script
- Next.js frontend (TypeScript) with login, create/list ICSR and NER demo
- Optional spaCy NER (fallback implemented if model not installed)
- Docker Compose for full stack demo + healthchecks
- Basic unit tests and GitHub Actions CI

Demo credentials (seeded)
- admin: admin@demo / Admin123!
- user: user@demo / User123!

Quick start (Docker, recommended)
1. Clone repository
   git clone https://github.com/nuradevo/dms-showcase.git
   cd dms-showcase

2. Copy example env files
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env.local

   Edit backend/.env if you change DB connection.

3. Build and run
   docker compose up --build

4. (Optional) If migrations/seed didn't run automatically (check backend logs), run:
   docker compose exec backend alembic -c backend/alembic.ini upgrade head
   docker compose exec backend python -m app.seed_demo

5. Open:
   - Frontend: http://localhost:3000
   - Backend API docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

Running locally without Docker (dev)
- Backend:
  cd backend
  python -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
  uvicorn app.main:app --reload --port 8000

- Frontend:
  cd frontend
  npm ci
  cp .env.example .env.local
  npm run dev

Testing
- Backend tests: cd backend && pytest -q

Adding spaCy model (optional, increases image size)
- To enable full spaCy NER, uncomment in backend/Dockerfile:
  RUN python -m spacy download ru_core_news_sm
- Or locally:
  python -m spacy download ru_core_news_sm

Badge & demo GIF
- The CI badge is shown at the top. To include a demo GIF:
  - Record a short screen capture (30–60s) showing: start app, login, create ICSR, run NER.
  - Save as `assets/demo.gif`
  - Add `![Demo](assets/demo.gif)` under this section.

Security notes
- This repo contains only synthetic/demo data.
- Do NOT commit real secrets. Ensure `.env` is in `.gitignore`.
- Change `JWT_SECRET` before any public deployment.

Contact
- Anastasia Fedina — byby10240@gmail.com — Moscow, Russia