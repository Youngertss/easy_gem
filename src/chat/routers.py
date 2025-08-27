from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket

from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.crud import db_save_message, db_get_last_messages
from src.chat.models import User

router = APIRouter(
    prefix="/ws/chat",
    tags=["chat"]
)

@router.websocket("/")
async def websocket_endpoint(
    websocket: WebSocket,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    await websocket.accept()
    
    auth_data = await websocket.receive_json()
    user_id = auth_data.get("user_id")
    username = auth_data.get("username")
    print("Greets to user:", username)
    
    init_mesages = await db_get_last_messages(10, session)   #last 10 msgs
    await websocket.send_json({"messages": init_mesages})  
    
    while True:
        data = await websocket.receive_json()
        await db_save_message(data_message=data, user_id=user_id, session=session)
        await websocket.send_json({"message": data["message"], "author": username, "timestamp":data["timestamp"]})
        print("User with that id sent a message:", user_id)
