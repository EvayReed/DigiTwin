import array
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
temperature = os.getenv("LLM_TEMPERATURE")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BACE_URL")


class LLMEngine:
    def __init__(self):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )

    async def reply(self, message: str):
        return (await self.llm.ainvoke(message)).content


class EmbeddingsEngine:
    def __init__(self):
        self.e_model = OllamaEmbeddings(
            model=model,
            base_url=base_url
        )

    def get_embedding_model(self):
        return self.e_model

    async def embed_documents(self, messages: List[str]):
        return self.e_model.embed_documents(messages)
