from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["upload files"])


@router.post("/add/pdf",
             summary="Upload PDF file",
             description="Upload PDF file",
             response_class=HTMLResponse)
async def add_pdf():
    return "pdf added!"


@router.post("/add/txt",
             summary="Upload TXT file",
             description="Upload TXT file",
             response_class=HTMLResponse)
async def add_pdf():
    return "pdf added!"
