import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.games.crud import db_get_game

pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"


# We can also use pytest.mark.parametrize(name, ("name1", "name2")) #to test several names etc
async def test_get_game(session: AsyncSession):
    game = await db_get_game(game_id=3, session=session)
    assert game.name == "Miner"

    game = await db_get_game(name="FortuneWheel", session=session)
    assert game.id == 1
