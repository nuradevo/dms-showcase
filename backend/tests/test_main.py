import pytest
from httpx import AsyncClient

from app.main import app

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

@pytest.mark.asyncio
async def test_ml_ner_fallback():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/ml/ner", json={"text": "Пациент принял Aspirin и почувствовал головную боль"})
    assert r.status_code == 200
    assert "entities" in r.json()