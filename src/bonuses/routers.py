from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session
from src.auth.auth import current_user
from src.auth.models import User
from src.bonuses.crud import db_get_current_bonuses, db_collect_super_bonuse


bonuses_router = APIRouter(
    prefix="/bonuses",
    tags=["bonuses"]
)


@bonuses_router.get("/current")
async def get_current_bonuses(session: AsyncSession = Depends(get_async_session)):
    result = db_get_current_bonuses(session)
    return result

@bonuses_router.patch("/collect_super_bonuse")
async def collect_super_bonuse(
    is_super: bool = False,
    session: AsyncSession = Depends(get_async_session), 
    user: User = Depends(current_user)
):
    result = db_collect_super_bonuse(is_super, session, user)
    return result