from fastapi import Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from src.games.models import Game, GameHistory, User, Tag, GameTag
from src.games.game_utils import wheelIncome

from random import randint
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone

async def db_get_fortune_wheel_event(session: AsyncSession, user: User):
    try:
        query = select(Game).where(Game.name=="FortuneWheel")
        result = await session.execute(query)
        fortune_wheel = result.scalars().first()
        fortune_wheel_data = fortune_wheel.data
        print(fortune_wheel_data)
        
        if round(user.balance,2) < fortune_wheel_data["cost"]:
            raise HTTPException(403, detail="Not enough credits")
        
        #get res
        event_res = wheelIncome(fortune_wheel_data)
        income = event_res["income"]
        user.balance += income - fortune_wheel_data["cost"]
        
        #add game to history
        stmt = insert(GameHistory).values(
            user_id = user.id,
            game_id = fortune_wheel.id,
            bet = Decimal(str(fortune_wheel.data["cost"])),
            income = Decimal(str(income)),
            played_at=datetime.now(timezone.utc),
            extra_data={}
        )
        await session.execute(stmt)
        
        await session.commit()
        return event_res
    except Exception as e:
        await session.rollback()
        raise HTTPException(400, detail=f"There is an error while processin fortune_wheel_event {e}")

async def db_get_safe_hack_event(sum_bet: Decimal, chance: float, coefficient: Decimal, expected_result: Decimal, session: AsyncSession, user: User):
    try:
        if user.balance < sum_bet:
            raise HTTPException(403, detail=f"Not enough credits")
        
        won = False
        random_num = randint(1,100)
        if random_num <= chance:
            won = True
            user.balance += expected_result - sum_bet
        else:
            user.balance -= sum_bet
            
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
            income = Decimal(str(income_sum)),
            played_at=datetime.now(timezone.utc),
            extra_data={"coefficient":float(coefficient), "chance": chance}
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

#miner end
async def db_finish_miner_event(sum_bet: Decimal, coefficient: Decimal, bombs_count: int, session: AsyncSession, user: User):
    try:
        prize = (sum_bet * coefficient).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        
        if prize < 0 and user.balance < -prize:
            prize = -user.balance

        income = prize
        user.balance += prize
        if prize < 0:
            income = Decimal("0")

        #add game to history
        query = select(Game).where(Game.name == "Miner")
        result = await session.execute(query)
        game = result.scalars().first()
            
        stmt = insert(GameHistory).values(
            user_id = user.id,
            game_id = game.id,
            bet = sum_bet,
            income = income,
            played_at=datetime.now(timezone.utc),
            extra_data={"coefficient": float(coefficient),"bombs_count": bombs_count}
        )
        await session.execute(stmt)

        await session.commit()
        return {"result": "success"}
    except Exception as e:
        await session.rollback()
        print("error while finishing Miner game", e)
