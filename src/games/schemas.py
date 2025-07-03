from datetime import datetime
from pydantic import BaseModel, Field

class DepositRequest(BaseModel):
    sum: int = Field(..., gt=0)

class TagCreate(BaseModel):
    name: str
    
class TagRead(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        extra = "ignore" #to ignore Tag.games

class GameBase(BaseModel):
    name: str
    game_type: str
    data: dict
    tags: list[int]
    photo: str
    created_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True
    
class GameRead(GameBase):
    id: int
    tags: list[TagRead]
    
    class Config:
        orm_mode = True

class GameCreate(GameBase):
    pass

class GameHistoryBase(BaseModel):
    user_id: int
    game_id: int
    income: int
    played_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True
    
class GameHistoryRead(GameHistoryBase):
    id: int

class GameHistoryCreate(GameHistoryBase):
    pass