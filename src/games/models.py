
from datetime import datetime

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Boolean, String, Integer, TIMESTAMP, JSON, ForeignKey

from src.auth.models import Game, GameHistory

# class Game(Base):
#     __tablename__="games"
#     id: Mapped[str] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     game_type: Mapped[str] = mapped_column(String)
#     data: Mapped[JSON] = mapped_column(JSON, nullable=False)
#     created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)


# class GameHistory(Base):
#     __tablename__="games_history"
#     id: Mapped[str] = mapped_column(Integer, primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
#     game_id: Mapped[int] = mapped_column(ForeignKey(Game.id), nullable=False)
#     income: Mapped[int] = mapped_column(String)
#     played_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow, nullable=False)
    
#     user = relationship("User", back_populates="games_history")
#     game = relationship("Game")
    