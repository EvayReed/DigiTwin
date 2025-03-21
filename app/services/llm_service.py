import array
from typing import List

from langchain_ollama import ChatOllama, OllamaEmbeddings
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

from openai import (
    APIError,
    AsyncAzureOpenAI,
    AsyncOpenAI,
    AuthenticationError,
    OpenAIError,
    RateLimitError,
)


load_dotenv()
temperature = os.getenv("LLM_TEMPERATURE")
model = os.getenv("LLM_MODEL")
base_url = os.getenv("LLM_BACE_URL")
api_key = os.getenv("OPENAI_API_KEY")

openaimodel = os.getenv("OPENAI_MODEL")
base_url = os.getenv("BASE_URL")



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

        self.openai_llm = OpenAI(
            model=openaimodel,
            temperature=0,
            max_retries=2,
            api_key=api_key, 
        )


        self.client = AsyncOpenAI(
            api_key=api_key, 
            base_url = base_url
        )

        self.openai_embeddings = OpenAIEmbeddings( 
            model="text-embedding-3-large", # 推荐的最新embedding模型 
            api_key=api_key )

    def get_embedding_model(self):
        return self.e_model

    def get_chat_model(self):
        return self.llm
    
    async def reply(self, message: str):
        return (await self.llm.ainvoke(message)).content

    def get_openai_model(self): 
        return self.openai_llm
    
    def get_openai_embeddings(self): 
        return self.openai_embeddings
    
    def get_client(self): 
        return self.client
    
    def reply_openai(self, 
                    message: str, 
                    # system_prompt: Optional[str] = None,
                    ) -> str: 
        try: 
            # messages = [] 
            # if system_prompt: 
            # messages.append({"role": "system", "content": system_prompt})
            # messages.append({"role": "user", "content": message}) 
            response = self.openai_llm.invoke( 
                message 
            ) 
            return response 
        except Exception as e: 
            return f"Error: {str(e)}"


ai_engine = AIEngine()

#test
# input_text = "The meaning of life is "
# print(ai_engine.get_client(input_text))
