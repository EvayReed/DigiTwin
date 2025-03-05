from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.services.vector_database_server import VectorDatabaseManager
import logging

router = APIRouter(tags=["upload files"])
logger = logging.getLogger(__name__)


def get_vector_database_manager():
    return VectorDatabaseManager()


@router.post("/add-file")
async def add_file(
        file: UploadFile = File(...),
        vector_database_manager: VectorDatabaseManager = Depends(get_vector_database_manager)
):
    try:
        result = await vector_database_manager.insertIntoVectorDB(file)
        return {"message": "File uploaded successfully", "content": result}
    except ValueError as e:
        logger.error(f"ValueError in add_file: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in add_file: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
