from fastapi import APIRouter
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket

from app.services.llm_service import LLMEngine

router = APIRouter(tags=["Chat"])
engine = LLMEngine()


@router.post("/chat",
             summary="Chat with AI",
             description="Simple conversation with AI")
async def chat_endpoint(message: str):
    try:
        response = await engine.reply(message)
        return {
            "state": 200,
            "message": response,
        }
    except Exception as e:
        return {
            "state": 500,
            "error": str(e),
        }


@router.websocket("/wsChat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await engine.reply(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
        await websocket.close()
