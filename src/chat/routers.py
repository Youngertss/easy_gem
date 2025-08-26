from fastapi import APIRouter, Depends, WebSocket, Query

from src.chat.crud import db_save_message, db_get_last_messages
from src.chat.models import User

router = APIRouter(
    prefix="/ws/chat",
    tags=["chat"]
)

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket, user: User):
    await websocket.accept()
    init_mesages = await db_get_last_messages()   #last 10 msgs
    await websocket.send(init_mesages)  
    
    while True:
        data = await websocket.receive_json()
        await db_save_message(data_message=data)
        await websocket.send_json(data)
