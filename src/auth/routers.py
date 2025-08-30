from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError
from src.auth.models import User
from src.auth.schemas import UserRead
from src.auth.auth import current_user
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_async_session

import shutil
import os
from uuid import uuid4

additional_users_router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@additional_users_router.get("/get_user_by_name/{username}", response_model=UserRead)
async def get_user_by_name(username: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(User).where(User.username==username)
        db_result = await session.execute(query)
        result = db_result.scalars().first()
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result
    except SQLAlchemyError as e:
        print(f"Error saving message to DB: {e}")

async def db_upload_photo(session: AsyncSession, currUser: User, file: UploadFile = File(...)):
    try:
        file_ext = os.path.splitext(file.filename)[1] #get file extantion
        filename = f"{uuid4().hex}{file_ext}" #unique name for pic to save
        file_path = os.path.join("src/imgs/", filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        if currUser.photo and currUser.photo!="/defaultUserPic.png":
            try:
                old_file_path = os.path.join("src/imgs/", currUser.photo.lstrip('/'))
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            except Exception as e:
                print(f"Failed to delete old photo: {e}")
    
        currUser.photo = "/"+filename
        
        await session.commit()
        return {"avatar_url": f"/{filename}"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"failed uploading photo (games/crud): {e}")

@additional_users_router.post("/upload_photo")
async def upload_photo (user: User = Depends(current_user), file: UploadFile = File(...), session: AsyncSession = Depends(get_async_session)):
    response = await db_upload_photo(session, user, file)
    return response
