from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import asc, desc, insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import SiteStatistic, User


async def db_get_leaderboard(limit: Optional[int] = 13, session: AsyncSession = None):
    try:
        stmt = (
            select(User)
            .where(User.total_earned > Decimal("10"))
            .order_by(desc(User.total_earned))
            .limit(limit)
        )
        result = await session.execute(stmt)
        result = result.scalars().all()

        return {"status": 200, "leaderboard": result}
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error while getting leaderboard: {e}"
        )


async def db_get_site_statistic(session: AsyncSession):
    try:
        statistic_db = await session.execute(select(SiteStatistic))
        statistic_db = statistic_db.scalars().first()
        return statistic_db
    except Exception as e:
        raise HTTPException(
            status_code=400, detail="Error while getting leaderboard: " + e
        )
