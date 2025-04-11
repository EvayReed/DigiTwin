from fastapi import APIRouter, File, UploadFile, HTTPException, Depends,Header
from fastapi.responses import JSONResponse
import base64

from app.core.utils.image_reader import ocr_request
from app.routes.chat import IndexType
from app.services.vector_database_server import vector_db_man
import logging
from app.core.utils.validate import get_token_from_header, handle_token_validation

router = APIRouter(tags=["upload files"])
logger = logging.getLogger(__name__)


@router.post("/add-file")
async def add_file(
        # delete
        authorization: str = Header(...),
        file: UploadFile = File(...),
):
    try:
        token = get_token_from_header(authorization)
        user_id = handle_token_validation(token)
        result = await vector_db_man.insert_into_vector_db(file, f'user_{user_id}')
        return {"message": "File uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# @router.post("/add-file-test")
# async def add_file(
#         authorization: str = Header(...),
#         file: UploadFile = File(...),
# ):
#     token = get_token_from_header(authorization)
#     user_id = handle_token_validation(token)
#     print(user_id)
#     result = await vector_db_man.insert_into_vector_db(file, f'user_{user_id}')
#     return {"message": "File uploaded successfully", "content": result}



@router.post("/describe-image/")
async def describe_image_endpoint(file: UploadFile = File(...)):
    file_content = await file.read()
    base64_string = base64.b64encode(file_content).decode('utf-8')

    image_content, res_dict = ocr_request(base64_string)

    return JSONResponse(content={"description": res_dict, "image_content": image_content})
