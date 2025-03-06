from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.services.memory_service import RunnableHistoryMemory
from app.services.llm_service import LLMEngine

router = APIRouter(tags=["memory_Chat"])

engine = LLMEngine()

memory = RunnableHistoryMemory(
    engine.get_llm(),
    n_message = 5
)

@router.post("/chat_memory",
             summary="Chat with memory",
             description="memory chat")
async def chat(message: str):
    try:
        response = memory.process_input(message)
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
