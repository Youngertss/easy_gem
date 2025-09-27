import csv
import json
import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from src.auth.models import Game, GameTag, Tag, SiteStatistic, User, GameHistory
from src.database import async_session_maker
from sqlalchemy import select, and_


seed_path = "src/seed_data"

async def create_init_records():
    async with async_session_maker() as session:
        # --- Tags ---
        with open(f"{seed_path}/tags.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            tags = []
            for row in reader:
                name = row["name"].strip('"')
                exists = await session.scalar(select(Tag).where(Tag.name == name))
                if not exists:
                    tags.append(Tag(name=name))
            session.add_all(tags)
        await session.commit()

        # --- Games ----
        with open(f"{seed_path}/games_data.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            games = []
            for row in reader:
                name = row["name"].strip('"')
                exists = await session.scalar(select(Game).where(Game.name == name))
                if not exists:
                    game = Game(
                        name=name,
                        photo=row["photo"].strip('"'),
                        game_type=row["game_type"].strip('"'),
                        data=json.loads(row["data"]),
                        created_at=datetime.fromisoformat(row["created_at"].strip('"')),
                    )
                    games.append(game)

            session.add_all(games)
        await session.commit()

        # ---GameTags ----
        with open(f"{seed_path}/game_tags.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            game_tags = []
            for row in reader:
                game_id = int(row["game_id"].strip('"'))
                tag_id = int(row["tag_id"].strip('"'))

                exists = await session.scalar(
                    select(GameTag).where(
                        and_(GameTag.game_id == game_id, GameTag.tag_id == tag_id)
                    )
                )
                if not exists:
                    game_tag = GameTag(game_id=game_id, tag_id=tag_id)
                    game_tags.append(game_tag)
            session.add_all(game_tags)
        await session.commit()

        # ---Statistics---
        result = await session.execute(select(SiteStatistic))
        if not result.scalars().first():
            statistic = SiteStatistic(
                total_earned=Decimal("0.00"),
                total_played=0,
                total_earned_today=Decimal("0.00"),
            )
            session.add(statistic)
            await session.commit()
        
        #--- Users ---
        with open(f"{seed_path}/users.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            users = []
            for row in reader:
                username = row["username"].strip('"')
                exists = await session.scalar(select(User).where(User.username == username))
                if not exists:
                    users.append(User(
                        id=int(row["id"].strip('"')),
                        username=username,
                        email=row["email"].strip('"'),
                        hashed_password=row["hashed_password"].strip('"'),
                        phone_number=row.get("phone_number"),
                        photo="/defaultUserPic.png",
                        balance=Decimal(row.get("balance", "0.00")),
                        total_deposit=Decimal(row.get("total_deposit", "0.00")),
                        total_withdrawn=Decimal(row.get("total_withdrawn", "0.00")),
                        total_withdrawals=int(row.get("total_withdrawals", 0)),
                        created_at=row.get("created_at", datetime.now(timezone.utc)),
                        favorite_game_id=row.get("favorite_game_id"),
                        total_earned=Decimal(row.get("total_earned", "0.00")),
                        total_played=int(row.get("total_played", 0))
                    ))
            session.add_all(users)
        await session.commit()

        #---GameHistory---
        with open(f"{seed_path}/games_history.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            history = []
            for row in reader:
                id = int(row["id"].strip('"'))
                exists = await session.scalar(select(GameHistory).where(GameHistory.id == id))
                if not exists:
                    history.append(GameHistory(
                        id=id,
                        user_id = int(row.get("user_id")),
                        game_id = int(row.get("game_id")),
                        income = Decimal(row.get("income")),
                        played_at = row.get("played_at"),
                        bet = Decimal(row.get("bet")),
                        extra_data = row.get("extra_data"),
                    ))
            session.add_all(history)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(create_init_records())


async def delete_records():
    async with async_session_maker as session:
        session.query(GameTag).detele()
        session.query(Game).detele()
        session.query(Tag).detele()
        session.commit()
