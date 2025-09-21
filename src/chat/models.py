from datetime import datetime

from pydantic import BaseModel

from src.auth.models import Message, User


class MessageSchema(BaseModel):
    id: int
    message: str
    author: str
    timestamp: datetime

    model_config = {"from_attributes": True}  # вместо from_orm
