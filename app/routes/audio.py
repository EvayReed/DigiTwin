from app.services.vector_database_server import VectorDatabaseManager
from fastapi import APIRouter, UploadFile, File, HTTPException
import logging
from openai import OpenAI
import tempfile
import os
import io
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
router = APIRouter(tags=["upload audio"])


@router.post("/audio-chat", summary="Recognize audio", description="Recognize speech from audio and convert to text")
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

        transcription_bytes = io.BytesIO(transcription.text.encode('gbk'))
        txt_file = UploadFile(filename="transcription.txt", file=transcription_bytes)
        vectorDatabaseManager = VectorDatabaseManager()
        try:
            await vectorDatabaseManager.insertIntoVectorDB(txt_file)
        except Exception as e:
            raise HTTPException(status_code=501, detail=f"Error insertIntoVectorDB: {e}")

        return {"text": transcription.text}
    except Exception as e:
        logger.error(f"Error in audio recognition: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
