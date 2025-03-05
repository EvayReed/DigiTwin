from fastapi import APIRouter, HTTPException
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

from app.services.llm_service import LLMEngine

router = APIRouter(tags=["Chat"])
engine = LLMEngine()


class ChatMessage(BaseModel):
    message: str


@router.post("/chat",
             summary="Chat with AI",
             description="Simple conversation with AI")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        response = await engine.reply(chat_message.message)
        return {"message": response}
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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
