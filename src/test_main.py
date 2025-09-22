from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, AsyncSession, create_async_engine, async_sessionmaker, AsyncTransaction
# from sqlalchemy import select, insert, and_, desc, inc

from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database import get_async_session
from src.main import app
from src.games.crud import db_get_game, db_get_user_history
from src.auth.routers import get_user_by_name


# DB_NAME change on DB_TEST_NAME
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL)


pytestmark = pytest.mark.anyio
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with async_engine.connect() as connection:
        yield connection


@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator[AsyncTransaction, None]:
    async with connection.begin() as transaction:
        yield transaction


# Use this fixture to get SQLAlchemy's AsyncSession.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in inner functions
@pytest.fixture()
async def session(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )

    yield async_session

    await transaction.rollback()


# Use this fixture to get HTTPX's client to test API.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in FastAPI's application endpoints
@pytest.fixture()
async def client(
    connection: AsyncConnection, transaction: AsyncTransaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session
    
    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_async_session]

    await transaction.rollback()


#-----TESTING----

# # @pytest.mark.anyio - we dont need this thx to "pytestmark = pytest.mark.anyio"
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works"}


async def test_get_user_history_db(session: AsyncSession):
    history = await db_get_user_history(2, session)
    history = history["history"]
    assert history


#We can also use pytest.mark.parametrize(name, ("name1", "name2")) #to test several names etc
async def test_get_game(session: AsyncSession):
    game = await db_get_game(game_id=3, session=session)
    assert game.name == "Miner"

    game = await db_get_game(name="FortuneWheel", session=session)
    assert game.id == 1


async def test_get_games_api():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
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



# pytest src/test_main.py -v\
