from fastapi import APIRouter, File, UploadFile
import tempfile
import os

from app.core.utils.files_util import MultiFileLoader

router = APIRouter(tags=["upload files"])


@router.post("/add/pdf")
async def add_pdf(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        loader = MultiFileLoader(tmp_path)
        pages = loader.load()

        full_text = "\n".join([page.page_content for page in pages])

        print(f"PDF Content:\n{full_text}")

        return {"content": full_text}

    finally:
        os.unlink(tmp_path)