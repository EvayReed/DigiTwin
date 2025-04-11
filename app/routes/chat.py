from fastapi import APIRouter, HTTPException
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from pydantic import BaseModel
import logging
from enum import Enum

from app.core.models.chat import ChatRequest
from app.core.utils.chart import chart
from app.core.utils.chat import chat
from app.services.vector_database_server import vector_db_man

logger = logging.getLogger(__name__)

from app.services.llm_service import ai_engine

router = APIRouter(tags=["Chat"])


class ChatMessage(BaseModel):
    message: str


class IndexType(str, Enum):
    Private = "Private"
    Normal = "Normal"
    Wealth = "Wealth"


# @router.post("/chat",
#              summary="Chat with AI",
#              description="Simple conversation with AI")
# async def chat_endpoint(chat_message: ChatMessage):
#     try:
#         response = await ai_engine.reply(chat_message.message)
#         return {"code": 200, "message": response}
#     except Exception as e:
#         logger.error(f"Error in chat_endpoint: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", summary="Chat with KnowledgeBase", description="Chat with your knowledge base")
async def query_knowledge_base(request: ChatRequest):
    try:
        result = chat(request.query, "sdm")
        return result
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/getChartDataIfNeeded", summary="getChartDataIfNeeded",
             description="The purpose of this method is to "
                         "determine whether the chart chart "
                         "needs to be generated, if it does, "
                         "it returns the chart data, "
                         "and if it does not, it returns "
                         "false"
)
async def getChartDataIfNeeded(request: ChatRequest):
    try:
        result = chart(request.query)
        return {
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.websocket("/wsChat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await ai_engine.reply(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
        await websocket.close()
