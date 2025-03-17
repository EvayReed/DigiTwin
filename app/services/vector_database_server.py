import logging
from typing import List
from fastapi import UploadFile
import os
import tempfile
from app.core.utils.files_util import MultiFileLoader
from app.services.llm_service import ai_engine
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".doc", ".docx", ".xls", ".xlsx"}


def format_text(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    data = []

    current_message = None

    for line in lines:
        line = line.strip()

        if len(line) > 19 and line[19] == ' ':
            if current_message:
                data.append(current_message)

            timestamp = line[:19]  # 时间戳部分
            user = line[20:]  # 用户部分

            current_message = {
                "timestamp": timestamp,
                "user": user,
                "message": ""
            }

        elif current_message:
            current_message["message"] += line  # 拼接消息内容

    if current_message:
        data.append(current_message)

    return data


class VectorDatabaseManager:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    async def insert_into_vector_db2(self, file: UploadFile, index_path: str) -> List[str]:
        index_path = self._format_path(index_path)
        tmp_path = None
        try:
            file_extension = await self._validate_file_extension(file.filename)
            tmp_path = await self._process_uploaded_content(file, file_extension)
            texts = format_text(tmp_path)
            self._update_or_create_faiss_index(ai_engine.get_embedding_model(), texts, index_path)
            return texts
        except IOError as e:
            logging.error(f"Data ingestion error: {e}")
            raise RuntimeError("Data ingestion error") from e
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    async def insert_into_vector_db(self, file: UploadFile, index_path: str) -> List[str]:
        index_path = self._format_path(index_path)
        tmp_path = None
        try:
            file_extension = await self._validate_file_extension(file.filename)
            tmp_path = await self._process_uploaded_content(file, file_extension)
            loader = MultiFileLoader(tmp_path)
            documents = loader.load()
            texts = self.text_splitter.split_documents(documents)
            self._update_or_create_faiss_index(ai_engine.get_embedding_model(), texts, index_path)
            return texts
        except IOError as e:
            logging.error(f"Data ingestion error: {e}")
            raise RuntimeError("Data ingestion error") from e
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def query_knowledge_base(self, query: str, index_path: str) -> List[str]:
        index_path = self._format_path(index_path)
        try:
            db = FAISS.load_local(index_path, ai_engine.get_embedding_model(), allow_dangerous_deserialization=True)
            qa = RetrievalQA.from_chain_type(
                llm=ai_engine.get_chat_model(),
                chain_type="stuff",
                retriever=db.as_retriever(search_kwargs={"k": 4})
            )
            return qa.invoke(query)
        except Exception as e:
            raise RuntimeError("Error while querying knowledge base") from e

    @staticmethod
    def _format_path(index_path: str) -> str:
        return f"app/store/{index_path}"

    @staticmethod
    def _update_or_create_faiss_index(embeddings, texts, index_path: str):
        if os.path.exists(index_path):
            db = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
            db.add_documents(texts)
        else:
            db = FAISS.from_documents(texts, embeddings)
        db.save_local(index_path)

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


vector_db_man = VectorDatabaseManager()
