from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["upload files"])


@router.post("/add/pdf",
             summary="self-check program",
             description="When you see this message, it means that the Lord's light waves have successfully connected!",
             response_class=HTMLResponse)
async def add_pdf():
    return "pdf added!"


@router.post("/add/txt",
             summary="self-check program",
             description="When you see this message, it means that the Lord's light waves have successfully connected!",
             response_class=HTMLResponse)
async def add_pdf():
    return "pdf added!"
