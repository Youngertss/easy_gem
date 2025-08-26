from fastapi import Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from src.database import get_async_session
from src.chat.models import Message, User

async def db_save_message(data_message, user: User, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Message).values(user_id=user.id, message=data_message.message, timestamp=data_message.timestamp)
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Error saving message to DB: {e}")

async def db_get_last_messages(limit: int = 10, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = select(Message).options(
                selectinload(Message.user)
                ).order_by(
                    Message.timestamp.desc()
                ).limit(limit)
        result = await session.execute(stmt).scalars().all()
        print(result)
        print(type(result))
        return result
    except SQLAlchemyError as e:
        print(f"Error retrieving messages from DB: {e}")
        return []