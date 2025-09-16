from typing import Optional
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import SiteStatistic, User
from src.auth.auth import current_user
from src.statistics.crud import db_get_leaderboard, db_get_site_statistic

router = APIRouter(
    prefix="/staticstics",
    tags=["statistic"]
)

@router.get("/get_leaderboard")
async def get_leaderboard(limit: Optional[int] = 13, session: AsyncSession = Depends(get_async_session)):
    result = await db_get_leaderboard(limit, session)
    return result

@router.get("/get_site_statistic")
async def get_site_statistic(session: AsyncSession = Depends(get_async_session)):
    result = await db_get_site_statistic(session)
    return result
