from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.database import get_async_session
from src.games.schemas import GameRead, GameCreate, GameHistoryRead, GameHistoryCreate
from src.games.crud import db_create_game, db_get_game, db_get_all_games, db_add_game_history, db_get_user_history

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

@router.post("/create_game")
async def create_game(game_info: GameCreate, session: AsyncSession = Depends(get_async_session)):
    await db_create_game(game_info, session)
    return {"status":"success"}

@router.get("/get_game", response_model = GameRead)
async def get_game(id: int, session: AsyncSession = Depends(get_async_session)):
    game = await db_get_game(id, session)
    return game

@router.get("/get_all_games")
async def get_all_games(session: AsyncSession = Depends(get_async_session)):
    games = await db_get_all_games(session)
    return games

@router.post("/add_game_history")
async def add_game_history(game_info: GameHistoryCreate, session: AsyncSession = Depends(get_async_session)):
    await db_add_game_history(game_info, session)
    return {"status":"success"}

@router.get("/get_user_history")
async def get_user_history(user_id: int, session: AsyncSession = Depends(get_async_session)):
    games_history = await db_get_user_history(user_id, session)
    return games_history


