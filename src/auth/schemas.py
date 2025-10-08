from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Union

from fastapi_users import models, schemas


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    username: str
    email: str
    phone_number: str
    photo: str
    balance: Decimal
    total_deposit: Decimal
    deposit_bonus_multiplier: Decimal
    total_earned: Decimal
    total_played: int
    total_withdrawn: Decimal
    total_withdrawals: int
    created_at: datetime
    favorite_game_id: Union[int, None]


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    phone_number: str
    password: str
    created_at: datetime = datetime.now(timezone.utc)


class UserUpdate(schemas.BaseUserUpdate):
    pass
