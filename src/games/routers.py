from fastapi import APIRouter, Depends, UploadFile, File, Form, Query
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.database import get_async_session
from src.games.schemas import GameRead, GameCreate, GameHistoryRead, GameHistoryCreate, TagRead, TagCreate
from src.games.crud import (db_create_game, db_get_game, db_get_all_games, db_add_game_history, 
                            db_get_user_history, db_upload_photo, db_get_tags, db_create_tag)
from src.auth.auth import current_user
from src.auth.models import User

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

users_update_router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@users_update_router.post("/upload_photo")
async def upload_photo (user: User = Depends(current_user), file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    response = await db_upload_photo(session, user, file)
    return response


@router.post("/create_game")
async def create_game(game_info: GameCreate, session: AsyncSession = Depends(get_async_session)):
    await db_create_game(game_info, session)
    return {"status":"success"}

@router.get("/get_game", response_model = GameRead)
async def get_game(id: int, session: AsyncSession = Depends(get_async_session)):
    game = await db_get_game(id, session)
    return game

@router.get("/get_all_games")
async def get_all_games(session: AsyncSession = Depends(get_async_session), tag: Optional[str] = Query(default=None)):
    games = await db_get_all_games(session, tag)
    return games

@router.post("/add_game_history")
async def add_game_history(game_info: GameHistoryCreate, session: AsyncSession = Depends(get_async_session)):
    await db_add_game_history(game_info, session)
    return {"status":"success"}

@router.get("/get_user_history")
async def get_user_history(user_id: int, session: AsyncSession = Depends(get_async_session)):
    games_history = await db_get_user_history(user_id, session)
    return games_history

@router.post("/create_tag")
async def create_tag(name: str, session: AsyncSession = Depends(get_async_session)):
    result = await db_create_tag(name, session)
    return result

@router.get("/get_tags")
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    tags = await db_get_tags(session)
    return tags

# @router.get("/get_fortune_wheel_event")

# fortunewheel api