from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
load_dotenv()


class AIEngine:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            max_retries=2
        )

        self.e_model = OpenAIEmbeddings(
            model="text-embedding-3-large",
        )

    def get_embedding_model(self):
        return self.e_model

    def get_chat_model(self):
        return self.llm

    def get_openai_model(self):
        return self.llm

    async def reply(self, message: str):
        return (await self.llm.ainvoke(message)).content


ai_engine = AIEngine()
