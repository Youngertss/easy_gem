
from typing import Union
from datetime import date, datetime

from fastapi_users import schemas, models


class UserRead(schemas.BaseUser[int]):
    id: models.ID
    username: str
    email: str
    phone_number: str
    photo: str
    balance: int
    total_deposit: int
    total_withdrawn: int
    total_withdrawals: int
    created_at: datetime
    favorite_game_id: Union[int, None]

class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    phone_number: str
    password: str
    created_at: datetime = datetime.utcnow
    

class UserUpdate(schemas.BaseUserUpdate):
    pass