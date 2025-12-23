import pytest
from httpx import AsyncClient

from app.main import app

@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

@pytest.mark.asyncio
async def test_icrs_requires_auth():
    # Trying to create an ICSR without auth should be rejected (401)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.post("/icrs", json={"title": "t", "narrative": "n"})
    assert r.status_code in (401, 422)  # 401 Unauthorized or 422 if validation before auth