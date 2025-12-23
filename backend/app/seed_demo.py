# backend/app/seed_demo.py
import asyncio
from .database import AsyncSessionLocal, engine
from . import models, crud
from sqlalchemy.ext.asyncio import AsyncSession

async def seed():
    async with AsyncSessionLocal() as db:  # type: AsyncSession
        # create demo admin and user
        admin = await crud.get_user_by_email(db, "admin@demo")
        if admin is None:
            await crud.create_user(db, email="admin@demo", password="Admin123!", full_name="Admin Demo", role="admin")
        user = await crud.get_user_by_email(db, "user@demo")
        if user is None:
            await crud.create_user(db, email="user@demo", password="User123!", full_name="User Demo", role="user")
        # create small number of icrs
        for i in range(1,4):
            await crud.create_icsr(db, title=f"ICSR demo {i}", narrative=f"Это тестовый нарратив {i}", created_by_id=1)

if __name__ == "__main__":
    asyncio.run(seed())
    print("Seeding finished")
