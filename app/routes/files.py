from fastapi import APIRouter, File, UploadFile, HTTPException
import tempfile
import os

from app.core.utils.files_util import MultiFileLoader

router = APIRouter(tags=["upload files"])

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx", ".xls", ".xlsx"}


@router.post("/add-file")
async def add_file(file: UploadFile = File(...)):
    file_extension = os.path.splitext(file.filename)[-1].lower()
    if file_extension not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}. Supported types: {SUPPORTED_EXTENSIONS}"
        )

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        loader = MultiFileLoader(tmp_path)
        pages = loader.load()
        full_text = "\n".join([page.page_content for page in pages])
        return {"content": full_text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading file{e}")

    finally:
        os.unlink(tmp_path)
