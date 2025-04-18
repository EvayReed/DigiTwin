from fastapi import APIRouter
from .files import router as files_router
from .pdf import router as pdf_router

router = APIRouter()

router.include_router(files_router, prefix="/files", tags=["files"])
router.include_router(pdf_router, prefix="/pdf", tags=["pdf"])
