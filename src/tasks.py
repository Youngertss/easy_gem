import time
from decimal import Decimal
from datetime import datetime, timezone

from src.celery_app import celery, session_maker
from sqlalchemy import select, insert
from src.auth.models import Game, GameHistory

@celery.task(name="test_task")
def test_task(time_towait, res):
    time.sleep(time_towait)
    return res

@celery.task(name="add_game_history_task")
def add_game_history_task(game_name, user_id, sum_bet, income_sum, extra_data):
    with session_maker() as session:
        try:
            query = select(Game).where(Game.name == game_name)
            game = session.execute(query).scalars().first()

            stmt = insert(GameHistory).values(
                user_id=user_id,
                game_id=game.id,
                bet=Decimal(str(sum_bet)),
                income=Decimal(str(income_sum)),
                played_at=datetime.now(timezone.utc),
                extra_data=extra_data
            )
            session.execute(stmt)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e