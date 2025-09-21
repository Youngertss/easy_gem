from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import current_user
from src.auth.models import User
from src.database import get_async_session
from src.games.crud import (
    db_add_game_history,
    db_create_game,
    db_create_tag,
    db_deposit,
    db_get_all_games,
    db_get_game,
    db_get_tags,
    db_get_user_history,
)
from src.games.crud_events import (
    db_finish_miner_event,
    db_get_fortune_wheel_event,
    db_get_safe_hack_event,
)
from src.games.game_utils import get_start_miner_data
from src.games.schemas import (
    DepositRequest,
    GameCreate,
    GameHistoryCreate,
    GameHistoryRead,
    GameRead,
    TagCreate,
    TagRead,
)

router = APIRouter(prefix="/games", tags=["Games"])


@router.patch("/deposit")
async def deposit(
    data: DepositRequest,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    print(user)
    response = await db_deposit(data.sum, session, user)
    return response


@router.post("/create_game")
async def create_game(
    game_info: GameCreate, session: AsyncSession = Depends(get_async_session)
):
    await db_create_game(game_info, session)
    return {"status": "success"}


@router.get("/get_game", response_model=GameRead)
async def get_game(
    id: Optional[int] = None,
    name: Optional[str] = None,
    session: AsyncSession = Depends(get_async_session),
):
    if id is not None:
        return await db_get_game(id, None, session)
    elif name is not None:
        return await db_get_game(None, name, session)
    else:
        raise HTTPException(status_code=400, detail="Provide either id or name")


@router.get("/get_all_games")
async def get_all_games(session: AsyncSession = Depends(get_async_session)):
    games = await db_get_all_games(session)
    return games


@router.post("/add_game_history")
async def add_game_history(
    game_info: GameHistoryCreate, session: AsyncSession = Depends(get_async_session)
):
    await db_add_game_history(game_info, session)
    return {"status": "success"}


@router.get("/get_user_history/{user_id}")
async def get_user_history(
    user_id: int,
    last_id: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session),
):
    games_history = await db_get_user_history(user_id, session, last_id)
    return games_history


@router.post("/create_tag")
async def create_tag(name: str, session: AsyncSession = Depends(get_async_session)):
    result = await db_create_tag(name, session)
    return result


@router.get("/get_tags")
async def get_tags(session: AsyncSession = Depends(get_async_session)):
    tags = await db_get_tags(session)
    return tags


@router.get("/get_fortune_wheel_event")
async def get_fortune_wheel_event(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    fortune_wheel_event_data = await db_get_fortune_wheel_event(session, user)
    return fortune_wheel_event_data


@router.get("/get_safe_hack_event")
async def get_safe_hack_event(
    sum_bet: Decimal,
    chance: float,
    coefficient: Decimal,
    expected_result: Decimal,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    safe_hack_event_event_data = await db_get_safe_hack_event(
        sum_bet, chance, coefficient, expected_result, session, user
    )
    return safe_hack_event_event_data


@router.get("/start_miner_event")
async def start_miner_event(
    sum_bet: Decimal, bombs_count: int, user: User = Depends(current_user)
):
    if user.balance < sum_bet:
        raise HTTPException(status_code=403, detail="not enough credits")
    start_miner_evevnt_data = get_start_miner_data(bombs_count)
    return start_miner_evevnt_data


@router.get("/finish_miner_event")
async def finish_miner_event(
    sum_bet: Decimal,
    coefficient: Decimal,
    bombs_count: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    # if coefficient = -1 - user lost
    result = await db_finish_miner_event(
        sum_bet, coefficient, bombs_count, session, user
    )
    return result
