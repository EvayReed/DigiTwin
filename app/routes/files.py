from datetime import datetime
import os

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
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


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 获取文件的扩展名
        file_extension = file.filename.split('.')[-1]

        # 获取当前时间戳并构造新的文件名
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        new_filename = f"{timestamp}.{file_extension}"

        # 构造文件保存路径
        file_path = os.path.join(assets_folder, new_filename)

        # 将文件保存到指定路径
        with open(file_path, "wb") as f:
            f.write(await file.read())

        return JSONResponse(content={"message": "File uploaded successfully", "filename": new_filename},
                            status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
