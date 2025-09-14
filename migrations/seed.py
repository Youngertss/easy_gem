import csv
import json
import asyncio
from datetime import datetime

from src.auth.models import Game, GameTag, Tag
from src.database import async_session_maker
from sqlalchemy import select, and_


async def create_init_records():
    async with async_session_maker() as session:
        # --- Tags ---
        with open("src/games/tags.csv", "r", encoding="utf-8") as f:
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
        with open("src/games/games_data.csv", "r", encoding="utf-8") as f:
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
                        created_at=datetime.fromisoformat(row["created_at"].strip('"'))
                    )
                    games.append(game)

            session.add_all(games)
        await session.commit()

        #---GameTags ----
        with open("src/games/game_tags.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            game_tags = []
            for row in reader:
                game_id=int(row["game_id"].strip('"'))
                tag_id=int(row["tag_id"].strip('"'))

                exists = await session.scalar(select(GameTag).where(and_(
                    GameTag.game_id == game_id,
                    GameTag.tag_id == tag_id
                    )))
                if not exists:
                    game_tag=GameTag(
                        game_id=game_id,
                        tag_id=tag_id
                    )
                    game_tags.append(game_tag)
            session.add_all(game_tags)
        await session.commit()

if __name__ == "__main__":
    asyncio.run(create_init_records())
                
async def delete_records():
    async with async_session_maker as session:
        session.query(GameTag).detele()
        session.query(Game).detele()
        session.query(Tag).detele()
        session.commit()