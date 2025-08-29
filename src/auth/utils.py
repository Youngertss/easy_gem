from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.auth.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from src.auth.models import User
from src.auth.schemas import UserRead

additional_users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@additional_users_router.get("/get_user_by_name/{username}", response_model=UserRead)
async def get_user_by_name(username: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.username==username)
        db_result = await session.execute(query)
        result = db_result.scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result
    except SQLAlchemyError as e:
        print(f"Error saving message to DB: {e}")

