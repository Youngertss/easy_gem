from fastapi import Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from src.games.models import Game, GameHistory, User, Tag, GameTag
from src.games.game_utils import wheelIncome

async def db_get_fortune_wheel_event(session: AsyncSession, user: User):
    try:
        query = select(Game).where(Game.name=="FortuneWheel")
        result = await session.execute(query)
        fortune_wheel = result.scalars().first()
        fortune_wheel_data = fortune_wheel.data
        print(fortune_wheel_data)
        
        if user.balance < fortune_wheel_data["cost"]:
        #     user.balance -= fortune_wheel.data["cost"]
        # else:
            raise HTTPException(403, detail="Not enough credits")
        
        #get res
        event_res = wheelIncome(fortune_wheel_data)
        income = event_res["income"]
        
        user.balance += income - fortune_wheel_data["cost"]
        
        await session.commit()
        # await session.refresh(user)
        # print(user.balance)
        # print(fortune_wheel.data["cost"])

        return event_res
    except Exception as e:
        raise HTTPException(400, detail=f"There is an error while processin fortune_wheel_event {e}")
    