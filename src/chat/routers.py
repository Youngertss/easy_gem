from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket

from src.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from src.chat.crud import db_save_message, db_get_last_messages

import redis.asyncio as aioredis
import json
import asyncio

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
    
    #redis channels
    redis = aioredis.from_url("redis://redis:6379/0")
    pubsub = redis.pubsub()
    await pubsub.subscribe("chat_channel")
    
    #user
    auth_data = await websocket.receive_json()
    user_id = auth_data.get("user_id")
    username = auth_data.get("username")
    print("Greets to user:", username)
    
    #init message (curr situation in chat)
    init_mesages = await db_get_last_messages(10, session)   #last 10 msgs
    await websocket.send_json({"messages": init_mesages})  
    
    async def listen_to_client():
        while True:
            #process and save data
            data = await websocket.receive_json()
            await db_save_message(data_message=data, user_id=user_id, session=session)
            data_to_send = {"message": data["message"], "author": username, "timestamp":data["timestamp"]}
            
            #redis publish + get_message
            await redis.publish("chat_channel", json.dumps(data_to_send))

    async def listen_to_redis():
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
            if message and message["type"] == "message":
                try:
                    data = json.loads(message["data"])  # message["data"] is bytes
                    await websocket.send_json(data)  #send it to the front-end
                    print("User " + data["author"] + "sent a message:", data["message"])
                except Exception as e:
                    print("Error while processing message from Redis:", e)
            await asyncio.sleep(0.01)  # wait a little bit to aviod 100% CPU
    
    #two corutines at the same time
    await asyncio.gather(listen_to_client(), listen_to_redis()) 
    