from src.auth.models import Message, User
from pydantic import BaseModel
from datetime import datetime

class MessageSchema(BaseModel):
    id: int
    message: str
    author: str
    timestamp: datetime
    
    model_config = {
        "from_attributes": True  # вместо from_orm
    }