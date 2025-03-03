from langchain_ollama import ChatOllama
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
