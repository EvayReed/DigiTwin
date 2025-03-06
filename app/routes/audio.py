from app.services.vector_database_server import VectorDatabaseManager
from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, FileResponse
import logging
from openai import OpenAI
import tempfile
import os
import io
import re
import shutil
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)
router = APIRouter(tags=["upload audio"])

from app.services.llm_service import LLMEngine
engine = LLMEngine()

import pyttsx3
audio_engine = pyttsx3.init()

cache_dir = "temp"

@router.post("/add-audio", summary="Recognize audio", description="Recognize speech from audio and convert to text")
async def recognize_audio(request: Request, audio_file: UploadFile = File(...)):
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


        try:
            response = await engine.reply(transcription.text)
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Error Chat Response: {e}")


        try:
            os.makedirs(cache_dir, exist_ok=True)
            temp_audio_path = tempfile.mktemp(suffix=".wav", dir=cache_dir).replace("\\", "/")
            cleaned_text = re.sub(r'[\n\t\r]', ' ', response)
            audio_engine.save_to_file(cleaned_text, temp_audio_path)
            audio_engine.runAndWait()

            # return FileResponse(temp_audio_path, media_type="audio/wav", headers={"Content-Disposition": "inline"})
            base_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/"
            return {"audio_content": transcription.text,
                    "chat_response": response,
                    "response_url": f"{base_url}{temp_audio_path}"}
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Error Return audio: {e}")

    except Exception as e:
        logger.error(f"Error in audio recognition: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
        if os.path.exists(cache_dir):
            all_files = [os.path.join(cache_dir, f) for f in os.listdir(cache_dir) if
                         os.path.isfile(os.path.join(cache_dir, f))]
            if len(all_files) > 5:
                all_files.sort(key=lambda x: os.path.getmtime(x))
                for old_file in all_files[:len(all_files) - 5]:
                    os.remove(old_file)


@router.get("/temp/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("temp", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
