import pytest
from httpx import ASGITransport, AsyncClient


pytestmark = pytest.mark.any


# async def test_get_current_bonuses(client: AsyncClient):
#     async with client as ac:
#         response = await ac.get("/bonuses/get_current_bonuses")
#     data = response.json()
#     print("BONUSES:", data)
#     assert isinstance(data, list)


async def test_collect_super_bonuse(client: AsyncClient):
    async with client as ac:
        response = await ac.patch("/bonuses/collect_super_bonuse", params={"is_super":True})
    data = response.json()
    print("SUPER BONUSE:", data)
    assert data["response"] == "ok"
