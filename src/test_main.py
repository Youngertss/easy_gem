from typing import AsyncGenerator

import pytest
from fastapi import Depends
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database import get_async_session
from src.main import app

# from fastapi.testclient import TestClient
# client = TestClient(app)


# DB_NAME change on DB_TEST_NAME
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=True)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def async_session():
    async with get_async_session() as session:
        yield session


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works"}


@pytest.mark.anyio
async def test_get_games():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/games/get_all_games")
    data = response.json()
    assert data["tags_amount"] != [] and data["tag_games"] != []
    assert data["tag_games"] != {}


# @pytest.mark.anyio
# @pytest.mark.parametrize("name", ["FortuneWheel"])
# async def test_get_game(name, async_session):
#     # Создаём игру вручную в БД
#     await async_session.execute(
#         """
#         INSERT INTO games (name, game_type, data, tags, photo, created_at)
#         VALUES (:name, :game_type, :data, :tags, :photo, :created_at)
#         """,
#         {
#             "name": name,
#             "game_type": "luck",
#             "data": {"min_bet": 10, "max_bet": 100},
#             "tags": [1, 2],
#             "photo": "http://example.com/wheel.png",
#             "created_at": datetime.utcnow(),
#         },
#     )
#     await async_session.commit()

#     # Запросим игру через API
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         response = await ac.get(f"/games/get_game?name={name}")

#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == name
#     assert data["extra_data"] != {}


# pytest src/test_main.py -v\
