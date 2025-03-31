from app.core.models.agent import AgentCreateRequest
from fastapi import APIRouter, Header, Depends, HTTPException
import logging
import os
from dotenv import load_dotenv

from app.core.utils.agent import add_agent
from app.core.utils.validate import get_token_from_header, handle_token_validation

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Agent"])


@router.post("/create-agent", summary="Create Agent", description="Create a new agent")
async def create_agent(
        agent_data: AgentCreateRequest,
        authorization: str = Header(...),
):
    token = get_token_from_header(authorization)
    user_id = handle_token_validation(token)

    try:
        new_agent = add_agent(
            user_id=user_id,
            name=agent_data.name,
            avatar=agent_data.avatar,
            voice=agent_data.voice,
            language=agent_data.language,
            personality=agent_data.personality
        )

        if new_agent:
            logger.info(f"Agent created successfully for user_id: {user_id}")
            return {"message": "Agent created successfully", "agent": new_agent}
        else:
            logger.error(f"Failed to create agent for user_id: {user_id}")
            raise HTTPException(status_code=500, detail="Failed to create agent")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
