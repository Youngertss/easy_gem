from fastapi import Depends, HTTPException, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from src.games.models import Game, GameHistory, User, Tag, GameTag
from src.games.game_utils import wheelIncome
from src.tasks import add_game_history_task

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
        sum_bet = float(fortune_wheel.data["cost"])
        income_sum = float(income)
        extra_data={}
        add_game_history_task.delay("FortuneWheel", user.id, sum_bet, income_sum, extra_data)
        
        await session.commit()
        await session.refresh(user)
        
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
            
        await session.commit()
        await session.refresh(user)

        income_sum = expected_result if won else 0
        extra_data={"coefficient":float(coefficient)}
        # celery task
        add_game_history_task.delay("SafeHack", user.id, sum_bet, income_sum, extra_data)

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
        user.balance += prize-sum_bet
        if prize < 0:
            user.balance+=sum_bet
            income = Decimal("0")

        await session.commit()
        await session.refresh(user) #without this line task wouldnt work

        #add game to history
        extra_data={"coefficient": float(coefficient),"bombs_count": bombs_count}
        add_game_history_task.delay("Miner", user.id, sum_bet, income, extra_data)

        return {"result": "success", "income":float(income)}
    except Exception as e:
        await session.rollback()
        print("error while finishing Miner game", e)
