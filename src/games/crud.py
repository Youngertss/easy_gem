from fastapi import Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

# from src.database import get_async_session
from src.games.models import Game, GameHistory
from src.games.schemas import GameRead, GameCreate, GameHistoryRead, GameHistoryCreate


async def db_create_game(game_info: GameCreate, session: AsyncSession):
    try:
        stmt = insert(Game).values(game_info.model_dump())
        await session.execute(stmt)
        await session.commit()
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't create the game: {e}")

async def db_get_game(game_id: int, session: AsyncSession):
    try:
        query = select(Game).where(Game.id == game_id)
        result = await session.execute(query)
        game = result.scalars().first()
        
        if not game:
            raise HTTPException(status_code=404, detail="Game not found")
        return game
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get the game: {e}")

async def db_get_all_games(session: AsyncSession):
    try:
        query = select(Game)
        result = await session.execute(query)
        return result.scalars().all()
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get games: {e}")
    
async def db_add_game_history(game_info: GameHistoryCreate, session: AsyncSession):
    try:
        stmt = insert(GameHistory).values(game_info.model_dump())
        await session.execute(stmt)
        await session.commit()
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't add the game to history: {e}")

async def db_get_user_history(user_id: int, session: AsyncSession):
    try:
        query = select(GameHistory).where(GameHistory.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=404, detail=f"Can't get user history: {e}")