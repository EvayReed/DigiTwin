from datetime import datetime
from pathlib import Path
import shutil
import os

from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.responses import JSONResponse
import base64
from app.core.utils.image_reader import ocr_request
from app.routes.chat import IndexType
from app.services.vector_database_server import vector_db_man
import logging

router = APIRouter(tags=["upload files"])
logger = logging.getLogger(__name__)


@router.post("/add-file")
async def add_file(
        file: UploadFile = File(...),
):
    try:
        result = await vector_db_man.insert_into_vector_db(file, "sdm")
        return {"message": "File uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/describe-image/")
async def describe_image_endpoint(file: UploadFile = File(...)):
    file_content = await file.read()
    base64_string = base64.b64encode(file_content).decode('utf-8')

    image_content, res_dict = ocr_request(base64_string)

    return JSONResponse(content={"description": res_dict, "image_content": image_content})

assets_folder = "assets"
if not os.path.exists(assets_folder):
    os.makedirs(assets_folder)


UPLOAD_DIR = Path("assets")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload/")
async def upload_file(request: Request):
    try:
        # 获取请求体中的原始数据
        body = await request.body()

        # 设置文件名（这里可以自定义）
        file_location = UPLOAD_DIR / "uploaded_file.txt"

        # 保存文件到指定目录
        with file_location.open("wb") as buffer:
            buffer.write(body)

        # 返回成功响应
        return JSONResponse(content={"message": "File uploaded successfully", "file_name": file_location.name})

    except Exception as e:
        # 出现错误时返回错误信息
        return JSONResponse(status_code=500, content={"error": f"Upload failed: {str(e)}"})


@router.post("/upload_image/")
async def upload_file(request: Request):
    try:
        file_name = request.query_params.get("file_name")

        if not file_name:
            return JSONResponse(content={"message": "File name is required"}, status_code=400)

        file_content = await request.body()

        logging.error(file_content)
        logging.error(file_name)

        file_location = f"assets/{file_name}"
        with open(file_location, "wb") as f:
            f.write(file_content)

        return JSONResponse(content={"message": "File uploaded successfully", "file_path": file_location},
                            status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)