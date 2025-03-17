from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from fastapi.responses import JSONResponse
import base64

from app.core.utils.image_reader import describe_image
from app.services.vector_database_server import vector_db_man
import logging

router = APIRouter(tags=["upload files"])
logger = logging.getLogger(__name__)


@router.post("/add-file")
async def add_file(
        index_path: str,
        file: UploadFile = File(...),
):
    try:
        result = await vector_db_man.insert_into_vector_db(file, index_path)
        return {"message": "File uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/describe-image/")
async def describe_image_endpoint(file: UploadFile = File(...)):
    logger.info(f"收到请求了")
    # 异步读取文件内容
    file_content = await file.read()
    # 将字节转换为 base64 字符串
    encoded_string = base64.b64encode(file_content)
    base64_string = encoded_string.decode('utf-8')

    # 添加前缀
    data_url = f"data:image/jpg;base64,{base64_string}"

    data = {
        "data": [
            {"image": data_url,
             "features": [], "languages": ["zh-CN"]}
        ]
    }
    description = describe_image(data)
    logger.info(f"Description: {description}")

    return JSONResponse(content={"description": description})
