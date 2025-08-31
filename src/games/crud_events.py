from fastapi import Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from src.games.models import Game, GameHistory, User, Tag, GameTag
from src.games.game_utils import wheelIncome

from random import randint
from decimal import Decimal
from datetime import datetime, timezone

async def db_get_fortune_wheel_event(session: AsyncSession, user: User):
    try:
        query = select(Game).where(Game.name=="FortuneWheel")
        result = await session.execute(query)
        fortune_wheel = result.scalars().first()
        fortune_wheel_data = fortune_wheel.data
        print(fortune_wheel_data)
        
        if user.balance < fortune_wheel_data["cost"]:
            raise HTTPException(403, detail="Not enough credits")
        
        #get res
        event_res = wheelIncome(fortune_wheel_data)
        income = event_res["income"]
        user.balance += income - fortune_wheel_data["cost"]
        
        #add game to history
        stmt = insert(GameHistory).values(
            user_id = user.id,
            game_id = fortune_wheel.id,
            bet = fortune_wheel.data["cost"],
            income = income,
            played_at=datetime.now(timezone.utc)
        )
        await session.execute(stmt)
        
        await session.commit()
        return event_res
    except Exception as e:
        await session.rollback()
        raise HTTPException(400, detail=f"There is an error while processin fortune_wheel_event {e}")

async def db_get_safe_hack_event(sum_bet: float, chance: int, expected_result: float, session: AsyncSession, user: User):
    try:
        if user.balance<sum_bet:
            raise HTTPException(403, detail=f"Not enough credits")
        
        won = False
        random_num = randint(1,100)
        if random_num <= chance:
            won = True
            user.balance += Decimal(str(expected_result)) - Decimal(str(sum_bet))
        else:
            user.balance -= Decimal(str(sum_bet))
            
        #add game to history
        query = select(Game).where(Game.name == "SafeHack")
        result = await session.execute(query)
        game = result.scalars().first()
        income_sum = 0
        if won:
            income_sum = expected_result
            
        stmt = insert(GameHistory).values(
            user_id = user.id,
            game_id = game.id,
            bet = sum_bet,
            income = income_sum,
            played_at=datetime.now(timezone.utc)
        )
        await session.execute(stmt)
            
        await session.commit()
        await session.refresh(user)
        
        data = {
            "won": won,
            "random_num": random_num,
            "new_balance": user.balance
        };
        
        return data
    except Exception as e:
        await session.rollback()
        raise HTTPException(400, detail=f"There is an error while processin safe_hack_event {e}")