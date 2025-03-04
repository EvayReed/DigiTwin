import logging
from typing import List

from fastapi import UploadFile
import os
import tempfile
from langchain.text_splitter import RecursiveCharacterTextSplitter


from app.core.utils.files_util import MultiFileLoader
from app.services.llm_service import EmbeddingsEngine

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx", ".xls", ".xlsx"}
engine = EmbeddingsEngine()


class VectorDatabaseManager:
    async def insertIntoVectorDB(self, file: UploadFile):
        tmp_path = None
        try:
            file_extension = await self._validate_file_extension(file.filename)
            tmp_path = await self._process_uploaded_content(file, file_extension)
            loader = MultiFileLoader(tmp_path)
            full_text = loader.load()
            text_chunks = self.splitSentences(full_text[0].page_content)
            await self.embeddingAndVectorDB(text_chunks)
            return text_chunks
        except IOError as e:
            raise RuntimeError("Data ingestion error") from e
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    @staticmethod
    async def _validate_file_extension(filename: str) -> str:
        ext = os.path.splitext(filename)[-1].lower()
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Invalid extension: {ext}. Valid: {SUPPORTED_EXTENSIONS}")
        return ext

    @staticmethod
    async def _process_uploaded_content(file: UploadFile, file_extension: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
            content = await file.read()
            tmp.write(content)
            return tmp.name

    @staticmethod
    def splitSentences(full_text):
        if full_text is not None:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=20,
                chunk_overlap=10,
                length_function=len,
                add_start_index=True
            )
            texts = text_splitter.split_text(full_text)
            return texts

    @staticmethod
    async def embeddingAndVectorDB(text_chunks: List[str]):
        result = await engine.embed_documents(text_chunks)
        print(result)
