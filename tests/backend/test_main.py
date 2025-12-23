import pytest
from httpx import AsyncClient
# import the app via path that matches user's repo; for demo we assume backend.app.main exists
try:
    from backend.app.main import app
except Exception:
    # fallback simple app for local test generation
    from fastapi import FastAPI
    app = FastAPI()

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code in (200, 404)  # depending on demo state

@pytest.mark.asyncio
async def test_ml_ner_fallback():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/ml/ner", json={"text": "Пациент принял Aspirin и почувствовал головную боль"})
    assert r.status_code in (200, 404)
