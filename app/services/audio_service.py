from fastapi import UploadFile, Request
from openai import OpenAI
import tempfile
import os
import re
import io
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

import pyttsx3
pyttsx3_engine = pyttsx3.init()

from app.services.vector_database_server import VectorDatabaseManager
vectorDatabaseManager = VectorDatabaseManager()

from app.services.llm_service import AIEngine
LLM_engine = AIEngine()


class AudioManager:

    def __init__(self, cache_dir="cache_audio", AudioCacheMost=5):
        self.cache_dir = cache_dir
        self.AudioCacheMost = AudioCacheMost

    async def AudioToText(self, audio_file: UploadFile):
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
                return transcription.text
        except Exception as e:
            raise RuntimeError("Speech Recognition Error") from e
        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    async def TextToAudio(self, text: str):
        os.makedirs(self.cache_dir, exist_ok=True)
        temp_audio_path = tempfile.mktemp(suffix=".wav", dir=self.cache_dir).replace("\\", "/")
        pyttsx3_engine.save_to_file(text, temp_audio_path)
        pyttsx3_engine.runAndWait()
        return temp_audio_path

    async def AudioCacheLimit(self):
        if os.path.exists(self.cache_dir):
            all_files = [os.path.join(self.cache_dir, f) for f in os.listdir(self.cache_dir) if
                         os.path.isfile(os.path.join(self.cache_dir, f))]
            if len(all_files) > self.AudioCacheMost:
                all_files.sort(key=lambda x: os.path.getmtime(x))
                for old_file in all_files[:len(all_files) - self.AudioCacheMost]:
                    os.remove(old_file)

    async def TextInsertVectorDB(self, text: str):
        txt_file = UploadFile(filename="transcription.txt", file=io.BytesIO(text.encode('gbk')))
        await vectorDatabaseManager.insert_into_vector_db(txt_file)

    async def AudioToAudio(self, request: Request, audio_file: UploadFile):
        try:
            transcription_text = await self.AudioToText(audio_file)
            # await self.TextInsertVectorDB(transcription_text)
            # prompt = "(Please answer in plain text only, as I will need to convert your response to speech later. Do not include any formatting such as formulas. Here are the inputs:)"
            # reply_text = await LLM_engine.reply(prompt + transcription_text)
            reply_text = await LLM_engine.reply(transcription_text)
            reply_audio_path = await self.TextToAudio(reply_text)
            base_url = f"{request.url.scheme}://{request.url.hostname}:{request.url.port}/"
            return {"audio_content": transcription_text,
                    "chat_reply": reply_text,
                    "reply_audio": f"{base_url}{reply_audio_path}"}
        except Exception as e:
            raise RuntimeError("Audio Service Error") from e
        finally:
            await self.AudioCacheLimit()
