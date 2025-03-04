from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.vector_database_server import VectorDatabaseManager

router = APIRouter(tags=["upload files"])


@router.post("/add-file")
async def add_file(file: UploadFile = File(...)):
    vectorDatabaseManager = VectorDatabaseManager()
    try:
        result = await vectorDatabaseManager.insertIntoVectorDB(file)
        return {"message": "File uploaded successfully", "content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading file{e}")
