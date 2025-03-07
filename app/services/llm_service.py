import array
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
temperature = os.getenv("LLM_TEMPERATURE")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BACE_URL")


class AIEngine:
    def __init__(self):
        # Initialize the ChatOllama model with the given model, temperature, and base_url
        self.llm = ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url
        )
        # Initialize the OllamaEmbeddings model with the given model and base_url
        self.e_model = OllamaEmbeddings(
            model=model,
            base_url=base_url
        )

    def get_embedding_model(self):
        return self.e_model

    def get_chat_model(self):
        return self.llm

    async def reply(self, message: str):
        return (await self.llm.ainvoke(message)).content


ai_engine = AIEngine()
