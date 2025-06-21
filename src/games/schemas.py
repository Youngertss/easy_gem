from datetime import datetime
from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    game_type: str
    data: dict
    tags: list
    photo: str
    created_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True
    
class GameRead(GameBase):
    id: int

class GameCreate(GameBase):
    pass

class TagCreate(BaseModel):
    name: str
    
class TagRead(BaseModel):
    id: int
    name: str
    games: list
    

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