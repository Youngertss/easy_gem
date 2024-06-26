
from datetime import datetime, date
from typing import Union

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, String, Integer, TIMESTAMP, ForeignKey, Boolean, JSON

from src.database import Base, async_engine
# from src.games.models import Game, GameHistory
class Game(Base):
    __tablename__="games"
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[str] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    game_type: Mapped[str] = mapped_column(String)
    data: Mapped[JSON] = mapped_column(JSON, nullable=False)
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)

class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    phone_number: Mapped[str] = mapped_column(String, nullable=True)
    photo: Mapped[int] = mapped_column(Integer, default=1)
    balance: Mapped[int] = mapped_column(Integer, default= 0)
    total_deposit: Mapped[int] = mapped_column(Integer, default=0)
    total_withdrawn: Mapped[int] = mapped_column(Integer, default = 0)
    total_withdrawals: Mapped[int] = mapped_column(Integer, default = 0)
    created_at: Mapped[str] =  mapped_column(TIMESTAMP, default = datetime.utcnow)

    favorite_game_id: Mapped[Union[int, None]] =  mapped_column(ForeignKey(Game.id), nullable = True)
    favorite_game = relationship("Game")
    games_history = relationship("GameHistory", back_populates="user")

class GameHistory(Base):
    __tablename__="games_history"
    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id), nullable=False)
    income: Mapped[int] = mapped_column(Integer)
    played_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
    user = relationship("User", back_populates="games_history")
    game = relationship("Game")
    



# async def create_db_and_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

    