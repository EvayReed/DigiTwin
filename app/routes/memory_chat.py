from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.services.memory_service import RunnableHistoryMemory
from app.services.llm_service import AIEngine

router = APIRouter(tags=["memory_Chat"])

engine = AIEngine()

memory = RunnableHistoryMemory(
    engine.get_chat_model(),
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


@router.websocket("/chat_memory/wsChat")
async def websocket_endpoint(websocket: WebSocket):
    wsChat_memory = RunnableHistoryMemory(
        engine.get_llm(),
    )
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await wsChat_memory.process_input(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
        await websocket.close()
