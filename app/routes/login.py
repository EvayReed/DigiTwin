import requests
from fastapi import APIRouter, HTTPException, Header
import logging
from pydantic import BaseModel

from app.core.utils.user import get_user_config

router = APIRouter(tags=["Login"])
logger = logging.getLogger(__name__)
GOOGLE_API_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"


def verify_google_token(access_token: str):
    response = requests.get(GOOGLE_API_URL, params={"id_token": access_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()


class LoginRequest(BaseModel):
    idToken: str


@router.post("/login",
             summary="Login",
             description="Login the app from Google")
def login(login_request: LoginRequest):
    token = login_request.idToken

    if not token:
        raise HTTPException(status_code=400, detail="Token is missing or invalid")

    user_info = verify_google_token(token)

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = get_user_config(
        user_id=user_info.get("sub"),
        name=user_info.get("name"),
        avatar=user_info.get("picture"),
        email=user_info.get("email"),
        token=token
    )

    return {
        "message": "Access granted",
        "access_token": result.get("access_token"),
        "user_config": result.get("user_config")
    }
