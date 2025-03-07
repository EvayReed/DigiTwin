from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
import os
import logging
logger = logging.getLogger(__name__)
router = APIRouter(tags=["upload audio"])

from app.services.audio_service import AudioManager
audio_engine = AudioManager()

@router.post("/add-audio", summary="Recognize audio", description="Recognize speech from audio and convert to text")
async def chat_by_audio(request: Request, audio_file: UploadFile = File(...)):
    try:
        response = await audio_engine.AudioToAudio(request, audio_file)
        return {
            "state": 200,
            "message": response,
        }
    except Exception as e:
        return {
            "state": 500,
            "error": str(e),
        }

@router.get("/temp/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("temp", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
