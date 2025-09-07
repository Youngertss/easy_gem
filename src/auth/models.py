from datetime import datetime
from typing import Union, Any
from decimal import Decimal

from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, String, Integer, TIMESTAMP, ForeignKey, JSON, text, DECIMAL
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TIMESTAMP
from sqlalchemy.sql import func

from src.database import Base


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    photo: Mapped[str] = mapped_column(String, default="/defaultUserPic.png", nullable=False)
    game_type: Mapped[str] = mapped_column(String, nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(PG_TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    tags: Mapped[list["Tag"]] = relationship(secondary="game_tags", back_populates="games")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    games: Mapped[list["Game"]] = relationship(secondary="game_tags", back_populates="tags")


class GameTag(Base):
    __tablename__ = "game_tags"
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), primary_key=True)
 

class User(Base, SQLAlchemyBaseUserTable[int]):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # исправлено с str на int
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    phone_number: Mapped[Union[str, None]] = mapped_column(String, nullable=True, server_default=None)
    photo: Mapped[str] = mapped_column(String, default="/defaultUserPic.png", nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL(12,2), server_default="0.0", default=0.0)
    total_deposit: Mapped[Decimal] = mapped_column(DECIMAL(12,2), server_default="0.00", default=Decimal("0.00"))
    total_withdrawn: Mapped[Decimal] = mapped_column(DECIMAL(12,2), server_default="0.00", default=Decimal("0.00"))
    total_withdrawals: Mapped[int] = mapped_column(Integer, server_default="0", default=0)
    created_at: Mapped[datetime] = mapped_column(PG_TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    favorite_game_id: Mapped[Union[int, None]] = mapped_column(ForeignKey(Game.id), nullable=True)
    favorite_game = relationship("Game")
    games_history = relationship("GameHistory", back_populates="user")


class GameHistory(Base):
    __tablename__ = "games_history"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)  # исправлено с str на int
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id), nullable=False)
    bet:Mapped[Decimal] = mapped_column(DECIMAL(12,2))
    income: Mapped[int] = mapped_column(DECIMAL(12,2))
    played_at: Mapped[datetime] = mapped_column(
        PG_TIMESTAMP(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    extra_data: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

    user = relationship("User", back_populates="games_history")
    game = relationship("Game")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(PG_TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False)

    user = relationship("User")
    
    @property
    def author(self):
        return self.user.username


# async def create_db_and_tables():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
