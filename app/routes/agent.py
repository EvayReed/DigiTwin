from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
import logging

from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain_community.tools import SceneXplainTool

from app.services.llm_service import ai_engine

tool = SceneXplainTool()

memory = ConversationBufferMemory(memory_key="chat_history")
agent = initialize_agent(
    [tool], ai_engine.get_openai_model(), memory=memory, agent="conversational-react-description", verbose=True
)


router = APIRouter(tags=["Agent"])
logger = logging.getLogger(__name__)


class AgentMessage(BaseModel):
    message: str


@router.post("/chat",
             summary="Chat with AI",
             description="Simple conversation with AI")
async def chat_endpoint(chat_message: AgentMessage):
    try:
        response = agent.run(
            input=(
                "What is in this image https://img2.baidu.com/it/u=3451164928,1611454231&fm=253&fmt=auto&app=138&f=JPEG?w=500&h=667 "
                "Is it movie or a game? If it is a movie, what is the name of the movie?"
            )
        )
        return {"code": 200, "message": response}
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
