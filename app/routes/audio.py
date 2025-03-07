from fastapi import APIRouter, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse
import os
import json
import logging
logger = logging.getLogger(__name__)
router = APIRouter(tags=["upload audio"])

from app.services.audio_service import AudioManager
audio_engine = AudioManager()

@router.post("/add-audio", summary="Recognize audio", description="Recognize speech from audio and convert to text")
async def chat_by_audio(request: Request, audio_file: UploadFile = File(...)):
    try:
        response = await audio_engine.AudioToAudio(request, audio_file)
        return {"message": response}
    except Exception as e:
        logger.error(f"Error Audio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cache_audio/{filename}")
async def get_file(filename: str):
    file_path = os.path.join("cache_audio", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}


from fastapi import WebSocket, WebSocketDisconnect

# WebSocket 路由
@router.websocket("/wsAudio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = await audio_engine.wsReply(data)
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected")
        await websocket.close()
