from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncTransaction,
    async_sessionmaker,
    create_async_engine,
)

from src.auth.auth import current_user
from src.auth.models import User
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from src.database import get_async_session
from src.main import app

# DB_NAME change on DB_TEST_NAME
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL)


pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"


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

    async def override_current_user():
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        user = await async_session.execute(select(User).where(User.id == 2))
        user = user.scalars().first()
        return user

    app.dependency_overrides[current_user] = override_current_user
    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_async_session] = override_get_async_session
    yield AsyncClient(app=app, base_url="http://test")
    del app.dependency_overrides[get_async_session]
    del app.dependency_overrides[current_user]

    await transaction.rollback()


# fixture to get user and give it to functions that
# have dependecies get_current_user
@pytest.fixture
async def user(session: AsyncSession):
    async def current_user_override():
        user = await session.execute(select(User).where(User.id == 2))
        user = user.scalars().first()
        return user

    app.dependency_overrides[current_user] = current_user_override
    yield user

    del app.dependency_overrides[get_async_session]


# pytest tests/ (-v - visible process of testing) (-s - visible prints)
