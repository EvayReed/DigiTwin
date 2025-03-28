import requests
from fastapi import APIRouter, HTTPException, Header
import logging

router = APIRouter(tags=["Login"])
logger = logging.getLogger(__name__)
GOOGLE_API_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"


def verify_google_token(access_token: str):
    response = requests.get(GOOGLE_API_URL, params={"id_token": access_token})
    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()


@router.get("/login",
            summary="Login",
            description="login the app from google")
def protected_resource(authorization: str = Header(...)):
    token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else None
    if not token:
        raise HTTPException(status_code=400, detail="Token is missing or invalid")

    # Verify the token
    user_info = verify_google_token(token)
    # You can store user_info in your session/database here if needed

    return {"message": "Access granted", "user_info": user_info}
