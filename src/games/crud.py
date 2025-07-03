from fastapi import Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from sqlalchemy import select, insert

from typing import Optional
import shutil
import os
from uuid import uuid4

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

async def db_get_game(game_id: int, session: AsyncSession):
    try:
        query = select(Game).where(Game.id == game_id).options(selectinload(Game.tags))
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

async def db_get_user_history(user_id: int, session: AsyncSession):
    try:
        query = select(GameHistory).where(GameHistory.user_id == user_id)
        result = await session.execute(query)
        return result.scalars().all()
    
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

async def db_deposit(sum: int, session: AsyncSession, user: User):
    if sum <= 0:
        raise HTTPException(status_code=400, detail="Deposit amount must be positive.")
    try:
        print(user)
        user.balance += sum
        await session.commit()
        await session.refresh(user)
        return {"updated_balance":user.balance}
    except Exception as e:
        await session.rollback()
        raise HTTPException(404, detail=f"Problems while DEP {e}")

async def db_upload_photo(session: AsyncSession, currUser: User, file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1] #get file extantion
        filename = f"{uuid4().hex}{file_ext}" #unique name for pic to save
        file_path = os.path.join("src/imgs/", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # query = select(User).where(User.id == user_id)
        # res = await session.execute(query)
        # currUser = res.scalars().first()
        
        if currUser.photo and currUser.photo!="/defaultUserPic.png":
            try:
                old_file_path = os.path.join("src/imgs/", currUser.photo.lstrip('/'))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            except Exception as e:
                print(f"Failed to delete old photo: {e}")
    
        currUser.photo = "/"+filename
        
        await session.commit()
        # await session.refresh(currUser)

        # print(currUser.photo)
        return {"avatar_url": f"/{filename}"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"failed uploading photo (games/crud): {e}")