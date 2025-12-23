#!/usr/bin/env bash
set -e

# Simple wait for Postgres to be ready
echo "Waiting for database..."
RETRIES=20
until python - <<PY
import os,sys,asyncio
from sqlalchemy.ext.asyncio import create_async_engine
url = os.getenv("DATABASE_URL")
if not url:
    sys.exit(0)
try:
    # attempt to create engine and connect then close
    engine = create_async_engine(url)
    async def try_connect():
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
    asyncio.get_event_loop().run_until_complete(try_connect())
    sys.exit(0)
except Exception as e:
    # signal waiting
    sys.exit(1)
PY
do
  echo "DB not ready - sleeping..."
  sleep 2
  RETRIES=$((RETRIES-1))
  if [ $RETRIES -le 0 ]; then
    echo "Database did not become ready - continuing anyway"
    break
  fi
done

# Run alembic migrations
if command -v alembic >/dev/null 2>&1; then
  echo "Applying Alembic migrations..."
  alembic -c backend/alembic.ini upgrade head || echo "Alembic upgrade failed (continuing)"
else
  echo "Alembic not installed in image"
fi

# Run seed script (idempotent expected)
echo "Running seed script..."
python -m app.seed_demo || echo "Seed script failed or already applied"

# Start app
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload