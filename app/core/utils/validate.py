from fastapi import HTTPException
from typing import Optional

from app.core.utils.user import get_user_by_token


def get_token_from_header(authorization: str) -> Optional[str]:
    if authorization.startswith("Bearer "):
        return authorization.split(" ")[1]
    return None


def handle_token_validation(token: Optional[str]) -> Optional[int]:
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing or invalid")

    user_info = get_user_by_token(token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Token is invalid")

    return user_info.userId
