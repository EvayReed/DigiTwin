from fastapi import UploadFile
import os
import tempfile
from app.core.utils.files_util import MultiFileLoader

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx", ".xls", ".xlsx"}


class VectorDatabaseManager:
    async def insertIntoVectorDB(self, file: UploadFile):
        file_extension = await self._validate_file_extension(file.filename)
        tmp_path = await self._process_uploaded_content(file, file_extension)
        try:
            loader = MultiFileLoader(tmp_path)
            pages = loader.load()
            full_text = "\n".join(page.page_content for page in pages)
            return full_text
        except IOError as e:
            raise RuntimeError("Data ingestion error") from e
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @staticmethod
    async def _validate_file_extension(filename: str) -> str:
        ext = os.path.splitext(filename)[-1].lower()
        return ext
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Invalid extension: {ext}. Valid: {SUPPORTED_EXTENSIONS}")

    @staticmethod
    async def _process_uploaded_content(file: UploadFile, file_extension: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
            content = await file.read()
            tmp.write(content)
            return tmp.name
