import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import Bonuse
from src.bonuses.crud import db_get_current_bonuses

pytestmark = pytest.mark.anyio


async def test_get_bonuses(session: AsyncSession):
    bonuses = await db_get_current_bonuses(session=session)
    assert len(bonuses) == 2

