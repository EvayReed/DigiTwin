import requests
from fastapi import APIRouter, HTTPException, Header
import logging
from pydantic import BaseModel

from app.core.utils.user import get_user_config
from app.core.utils.validate import get_token_from_header

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


@router.get("/login",
            summary="Login",
            description="login the app from google")
def protected_resource(authorization: str = Header(...)):
    token = get_token_from_header(authorization)
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing or invalid")

    user_info = verify_google_token(token)

    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_config = get_user_config(
        user_id=user_info.get("sub"),
        name=user_info.get("name"),
        avatar=user_info.get("picture"),
        email=user_info.get("email"),
        token=token
    )

    return {"message": "Access granted", "user_config": user_config}
