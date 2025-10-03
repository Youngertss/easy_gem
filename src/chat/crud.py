from datetime import datetime

from fastapi import Depends
from sqlalchemy import insert, select, desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.chat.models import Message, MessageSchema, User


async def db_save_message(
    data_message, user_id: int, session: AsyncSession = None
) -> None:
    try:
        timestamp = datetime.fromisoformat(
            data_message["timestamp"].replace("Z", "+00:00")
        )
        stmt = insert(Message).values(
            user_id=user_id, message=data_message["message"], timestamp=timestamp
        )
        await session.execute(stmt)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        print(f"Error saving message to DB: {e}")


async def db_get_last_messages(
    limit: int = 29, session: AsyncSession = None
) -> list[dict]:
    try:
        statement = (
            select(Message)
            .options(selectinload(Message.user))
            .order_by(desc(Message.timestamp))
            .limit(limit)
        )
        result = await session.execute(statement)
        messages = result.scalars().all()

        messages_json = [
            MessageSchema.model_validate(m).model_dump(mode="json") for m in messages
        ]
        # print(messages_json)
        return messages_json
    except SQLAlchemyError as e:
        print(f"Error retrieving messages from DB: {e}")
        return []
