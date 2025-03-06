from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
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
