import pytest
from httpx import ASGITransport, AsyncClient

pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"


async def test_login(client: AsyncClient):
    data = {"username": "youngerts@gmail.com", "password": "youngerts"}
    async with client as ac:
        response = await ac.post("/auth/jwt/login", json=data)
    print("RESPONSE", response.json())  # ERROR
    assert response.json()
