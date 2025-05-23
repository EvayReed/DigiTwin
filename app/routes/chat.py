from fastapi import APIRouter, HTTPException, Request,Header
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import logging
from enum import Enum
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.schema import SystemMessage, HumanMessage
from datetime import datetime

from app.services.vector_database_server import vector_db_man
from app.core.utils.validate import get_token_from_header, handle_token_validation

load_dotenv()

from app.core.models.chat import ChatRequest
from app.core.utils.chart import chart
from app.core.utils.chat import chat,stream_chat

logger = logging.getLogger(__name__)

from app.services.llm_service import ai_engine

router = APIRouter(tags=["Chat"])


class ChatMessage(BaseModel):
    message: str


class IndexType(str, Enum):
    Private = "Private"
    Normal = "Normal"
    Wealth = "Wealth"


@router.post("/aiChat", summary="Chat with AI", description="Simple conversation with AI")
async def chat_endpoint(chat_message: ChatMessage):
    try:
        llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2
        )

        async def generate():
            stream = llm.stream(chat_message.message)
            async for chunk in stream:
                yield chunk
                await asyncio.sleep(0)

        return StreamingResponse(generate(), media_type="text/plain")

    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", summary="Chat with KnowledgeBase", description="Chat with your knowledge base")
async def query_knowledge_base(request: ChatRequest):
    try:
        result = chat(request.query, "sdm")
        return result
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/queryRag", summary="Chat with KnowledgeBase", description="Chat with your knowledge base")
async def query_knowledge_base(request: ChatRequest):
    try:
        result = vector_db_man.query_knowledge_base(request.query, "sdm")
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


@router.post("/add-str")
async def add_str(
        request: ChatRequest,
        authorization: str = Header(...),
        ):
    try:
        token = get_token_from_header(authorization)
        user_id = handle_token_validation(token)
        # result = await vector_db_man.insert_into_vector_db_str(request.query, f'user_{user_id}')
        result = await vector_db_man.insert_into_vector_db_str(request.query, "sdm")
        return {"message": "str uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_str: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

class ChatMessage_Stream(BaseModel):
    query: str
    query_type: str

@router.post("/stream-chat")
async def chat_endpoint(
    chat_request: ChatMessage_Stream,
    authorization: str = Header(...),):
    try:
        token = get_token_from_header(authorization)
        user_id = handle_token_validation(token)
        generator = await stream_chat(
            query=chat_request.query,
            type=chat_request.query_type,
            ai_engine=ai_engine,
            user_id=user_id
        )
        return EventSourceResponse(generator)
    
    except Exception as e:
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
