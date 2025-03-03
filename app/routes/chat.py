from fastapi import APIRouter
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
