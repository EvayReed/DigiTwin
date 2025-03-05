from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
from openai import OpenAI
import tempfile
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
router = APIRouter(tags=["upload audio"])

@router.post("/add-audio", summary="Recognize audio" ,description="Recognize speech from audio and convert to text")
async def recognize_audio(audio_file: UploadFile = File(...)):
    try:
        audio_data = await audio_file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data)
            tmp_file_path = tmp_file.name
        with open(tmp_file_path, "rb") as file:
            client = OpenAI(api_key=api_key)
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=file)
        return {"text": transcription.text}

    except Exception as e:
        logger.error(f"Error in audio recognition: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

