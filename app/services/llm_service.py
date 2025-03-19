import array
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

load_dotenv()
temperature = os.getenv("LLM_TEMPERATURE")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BACE_URL")
api_key = os.getenv("OPENAI_API_KEY")


class AIEngine:
    def __init__(self):
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )
        self.e_model = OllamaEmbeddings(
            model=model,
            base_url=base_url
        )
        # self.e_model = OpenAIEmbeddings(model="text-embedding-3-large", api_key=api_key)
        self.open_llm = OpenAI(api_key=api_key)

    def get_embedding_model(self):
        return self.e_model

    def get_chat_model(self):
        return self.llm

    def get_openai_model(self):
        return self.open_llm

    async def reply(self, message: str):
        return (await self.llm.ainvoke(message)).content


ai_engine = AIEngine()
