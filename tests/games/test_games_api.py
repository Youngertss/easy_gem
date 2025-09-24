from datetime import datetime, timezone
from decimal import Decimal

from httpx import ASGITransport, AsyncClient

from src.main import app
from src.games.schemas import GameCreate, TagCreate, TagRead, GameRead


import pytest
pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"

async def test_root(client: AsyncClient):
    async with client as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works"}


async def test_get_games_api(client: AsyncClient):
    async with client as ac:
        response = await ac.get("/games/get_all_games")
    data = response.json()
    assert data["tags_amount"] != [] and data["tag_games"] != []
    assert data["tag_games"] != {}


@pytest.mark.parametrize("name", ("FortuneWheel",))
async def test_get_game_by_name_api(client: AsyncClient, name):
    async with client as ac:
        response = await ac.get(f"/games/get_game?name={name}")
    response = response.json()
    assert response["name"] == name


async def test_create_game(client: AsyncClient):
    async with client as ac:
        game = GameCreate(
            name="SweetyStrawberry",
            game_type="luck",
            data={"min_bet": 10, "max_bet": 100},
            tags=[1, 2],
            photo="http://example.com/wheel.png"
        )

        response = await ac.post(f"/games/create_game", json=game.model_dump(exclude={"created_at"}))
    response_game = response.json()

    assert response_game["name"]== "SweetyStrawberry"


async def test_get_tags(client: AsyncClient):
    async with client as ac:
        tags = await ac.get(f"/games/get_tags")
    tags = tags.json()
    assert isinstance(tags, list)
    assert tags[0]["id"] == 1


async def test_create_tag(client: AsyncClient):
    new_tag = TagCreate(name="vikings")
    async with client as ac:
        tag = await ac.post(f"/games/create_tag", json=new_tag.model_dump())

    # print(tag.json())
    tag = TagRead.model_validate(tag.json())

    assert tag.name == "vikings"
    assert isinstance(tag.id, int)

async def test_get_safe_hack_event(client: AsyncClient):
    data = {
        "sum_bet":Decimal("10.00"),
        "chance": 1.96,
        "coefficient": Decimal("2.00"),
        "expected_result": Decimal("20.00"),
        "testing": True
    }
    async with client as ac:
        response = await ac.get("/games/get_safe_hack_event", params=data)
    print("SAFEHACK",response, response.json())
    response = response.json()

    assert isinstance(response["won"], bool)