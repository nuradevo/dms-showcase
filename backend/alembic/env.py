import asyncio
from logging.config import fileConfig
import os
import sys
from sqlalchemy import pool
from sqlalchemy.engine import create_engine
from alembic import context

# Allow import of app package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
fileConfig(config.config_file_name)

# Import your metadata object (models.Base.metadata)
from app.models import Base  # noqa: E402
from app.database import DATABASE_URL  # noqa: E402

target_metadata = Base.metadata

def run_migrations_offline():
    url = DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    from sqlalchemy.ext.asyncio import create_async_engine
    connectable = create_async_engine(DATABASE_URL, poolclass=pool.NullPool)
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_async_migrations())