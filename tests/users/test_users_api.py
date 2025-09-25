import pytest
from httpx import ASGITransport, AsyncClient

from src.auth.routers import get_user_by_name

pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"

async def test_get_user_by_name(client:AsyncClient):
    username = "youngerts"
    async with client as ac:
        response = await ac.get(f"/users/get_user_by_name/{username}")
    print("USER BY USERNAME", response, response.json())

    assert response.json()["username"] == username