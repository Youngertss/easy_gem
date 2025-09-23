from sqlalchemy.ext.asyncio import AsyncSession

from src.games.crud import db_get_user_history

import pytest
pytestmark = pytest.mark.anyio
# @pytest.mark.anyio - we dont need this more thx to "pytestmark = pytest.mark.anyio"

async def test_get_user_history_db(session: AsyncSession):
    history = await db_get_user_history(2, session)
    history = history["history"]
    assert history