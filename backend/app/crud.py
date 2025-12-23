# backend/app/crud.py
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, auth
from typing import Optional

async def create_user(db: AsyncSession, email: str, password: str, full_name: Optional[str] = None, role: str = "user"):
    user = models.User(email=email, hashed_password=auth.hash_password(password), full_name=full_name, role=role)
    db.add(user)
    try:
        await db.commit()
        await db.refresh(user)
        return user
    except IntegrityError:
        await db.rollback()
        return None

async def get_user_by_email(db: AsyncSession, email: str):
    q = select(models.User).where(models.User.email == email)
    res = await db.execute(q)
    return res.scalars().first()

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not auth.verify_password(password, user.hashed_password):
        return None
    return user

async def create_icsr(db: AsyncSession, title: str, narrative: str, created_by_id: Optional[int] = None):
    icsr = models.ICSR(title=title, narrative=narrative, created_by_id=created_by_id)
    db.add(icsr)
    await db.commit()
    await db.refresh(icsr)
    return icsr

async def list_icrs(db: AsyncSession, limit: int = 50):
    q = select(models.ICSR).order_by(models.ICSR.id.desc()).limit(limit)
    res = await db.execute(q)
    return res.scalars().all()
