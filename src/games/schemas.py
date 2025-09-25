from datetime import datetime, timezone
from decimal import Decimal

from pydantic import BaseModel, Field


class DepositRequest(BaseModel):
    sum: Decimal = Field(..., gt=0)


class TagCreate(BaseModel):
    name: str


class TagRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True, "extra": "ignore"}


class GameBase(BaseModel):
    name: str
    game_type: str
    data: dict
    tags: list[int]
    photo: str
    created_at: datetime = datetime.now(timezone.utc)

    class Config:
        arbitrary_types_allowed = True


class GameRead(GameBase):
    id: int
    tags: list[TagRead]

    model_config = {"from_attributes": True, "extra": "ignore"}


class GameCreate(GameBase):
    pass


class GameHistoryBase(BaseModel):
    user_id: int
    game_id: int
    bet: Decimal
    income: Decimal
    played_at: datetime
    extra_data: dict

    class Config:
        arbitrary_types_allowed = True


class GameHistoryRead(GameHistoryBase):
    id: int


class GameHistoryCreate(GameHistoryBase):
    pass
