from fastapi import APIRouter, Depends, WebSocket

router = APIRouter(
    prefix="/ws/chat",
    tags=["chat"]
)

@router.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json(data)
