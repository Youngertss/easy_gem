from datetime import datetime
from pydantic import BaseModel

class GameBase(BaseModel):
    name: str
    game_type: str
    data: dict
    created_at: datetime = datetime.utcnow()
    
    class Config:
        arbitrary_types_allowed = True
    
class GameRead(GameBase):
    id: int

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