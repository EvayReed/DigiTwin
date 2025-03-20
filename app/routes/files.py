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
        index_path: IndexType,
        file: UploadFile = File(...),
):
    try:
        result = await vector_db_man.insert_into_vector_db2(file, index_path)
        return {"message": "File uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/describe-image/")
async def describe_image_endpoint(file: UploadFile = File(...)):
    # 异步读取文件内容
    file_content = await file.read()
    base64_string = base64.b64encode(file_content).decode('utf-8')

    description = ocr_request(base64_string)

    return JSONResponse(content={"description": description})
