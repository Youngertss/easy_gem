from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert, desc, and_

from typing import Optional
from decimal import Decimal

# from src.database import get_async_session
from src.games.models import Game, GameHistory, User, Tag, GameTag
from src.games.schemas import GameRead, GameCreate, GameHistoryRead, GameHistoryCreate

async def db_create_game(game_info: GameCreate, session: AsyncSession):
    try:
        
        result = await session.execute(select(Tag).where(Tag.id.in_(game_info.tags)))
        tags = result.scalars().all()
        
        if len(tags) != len(game_info.tags):
            raise HTTPException(status_code=400, detail="One or more tags not found")
        
        # stmt = insert(Game).values(game_info.model_dump())
        new_game = Game(
            name=game_info.name,
            photo=game_info.photo,
            game_type=game_info.game_type,
            data=game_info.data,
            tags=tags,
            created_at=game_info.created_at
        )
        session.add(new_game)
        await session.commit()
        await session.refresh(new_game)
        return new_game
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't create the game: {e}")

async def db_get_game(
        game_id: Optional[int] = None,
        name: Optional[str] = None,
        session: AsyncSession = None
    ):
    try:
        if game_id is not None:
            query = select(Game).where(Game.id == game_id).options(selectinload(Game.tags))
        elif name is not None:
            query = select(Game).where(Game.name == name).options(selectinload(Game.tags))
        else:
            raise HTTPException(status_code=400, detail="id or name is needed")
        
        result = await session.execute(query)
        game = result.scalars().first()
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get the game: {e}")


async def db_get_all_games(session: AsyncSession, tag: Optional[str] = None):
    try:
        if tag:
            query = (
                select(Game)
                .join(Game.tags)
                .where(Tag.name == tag)
                .options(selectinload(Game.tags)) #loading full tags, not only their ID's (on fast way by 1 additional query)
                .distinct()
            )
        else:
            query = select(Game).options(selectinload(Game.tags))

        result = await session.execute(query)
        return result.scalars().all()

    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Cant get games: {e}")
    
async def db_add_game_history(game_info: GameHistoryCreate, session: AsyncSession):
    try:
        stmt = insert(GameHistory).values(game_info.model_dump())
        await session.execute(stmt)
        await session.commit()
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't add the game to history: {e}")

async def db_get_user_history(user_id: int, session: AsyncSession, last_id):
    try:
        if last_id is not None:
            query = (
                select(GameHistory)
                .where(and_(
                    GameHistory.user_id == user_id,
                    GameHistory.id < last_id)
                    )
                .order_by(desc(GameHistory.played_at))
                .limit(20)
                .options(selectinload(GameHistory.game))
            )
        else:
            query = (
                select(GameHistory)
                .where(GameHistory.user_id == user_id)
                .order_by(desc(GameHistory.played_at))
                .limit(20)
                .options(selectinload(GameHistory.game))
            )
        result = await session.execute(query)
        history = result.scalars().all()
        has_more = len(history) == 20

        return {"history": history, "has_more": has_more}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get user history: {e}")

async def db_create_tag(name: str, session: AsyncSession):
    try:
        stmt = insert(Tag).values({"name":name})
        await session.execute(stmt)
        await session.commit()
        return "tag created"
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Cat't create tag: {e}")

async def db_get_tags(session: AsyncSession):
    try:
        query = select(Tag)
        result = await session.execute(query)
        return result.scalars().all()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get tags: {e}")

async def db_deposit(sum: Decimal, session: AsyncSession, user: User):
    if sum <= 1:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive and at least 1 dollaer")
    try:
        print(user)
        if user.balance > 9000000:
            raise HTTPException(400, detail="User have alreade has too much money")
        if sum > 1000000:
            raise HTTPException(400, detail="You can't dep more than 1.000.000 dollar per time")
        
        user.balance += sum
        user.total_deposit += sum
        await session.commit()
        await session.refresh(user)
        return {"updated_balance":user.balance}
    except Exception as e:
        await session.rollback()
        raise HTTPException(404, detail=f"Problems while DEP {e}")
