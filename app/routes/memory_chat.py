from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.services.memory_service import RunnableHistoryMemory
from app.services.llm_service import LLMEngine

router = APIRouter(tags=["memory_Chat"])

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You're an assistant who speaks in {language}. Respond in 20 words or fewer",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)


session_id = '111'
def get_session_history(session_id):
    return SQLChatMessageHistory(session_id, "sqlite:///memory.db")

engine = LLMEngine()

memory = RunnableHistoryMemory(get_session_history,engine.get_llm(),prompt,session_id)


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
