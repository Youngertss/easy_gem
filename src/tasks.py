import time
from decimal import Decimal
from datetime import datetime, timezone

from src.celery_app import celery, session_maker
from sqlalchemy import select, insert, desc, asc
from sqlalchemy.orm import selectinload
from src.auth.models import Game, GameHistory, User, SiteStatistic

@celery.task(name="test_task")
def test_task(time_towait, res):
    time.sleep(time_towait)
    return res

@celery.task(name="update_favorite_games_task")
def update_favorite_games_task():
    with session_maker() as session:
        try:
            users = session.execute(select(User))
            users = users.scalars().all()
            for user in users:
                query = (
                    select(GameHistory)
                    .where(GameHistory.user_id == user.id)
                    .order_by(desc(GameHistory.played_at))
                    .limit(100)
                )
                games_history = session.execute(query)
                games_history = games_history.scalars().all()

                counts = {}
                for item in games_history:
                    id = str(item.game_id)
                    if id in counts.keys():
                        counts[id] += 1
                    else:
                        counts[id] = 1

                fav_id = -1
                max_count = 0
                for id, count in counts.items():
                    if count > max_count:
                        fav_id = int(id)
                        max_count = count

                user.favorite_game_id = fav_id
                session.commit()
        except Exception as e:
            session.rollback()
            raise e

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