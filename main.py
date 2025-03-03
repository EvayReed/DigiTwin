from fastapi import FastAPI
from langchain_ollama import ChatOllama

app = FastAPI(
    title="AI Service API",
    version="1.0",
    description="LangChain API Deployment"
)

llm = ChatOllama(
    model="deepseek-r1:1.5b",
    temperature=0.7,
    base_url="http://localhost:11434"
)

@app.get("/",summary="welcome page",
          description="Tests the current running status of the service")
async def health():
    return "DigiTwin Server is running"


@app.post("/chat",summary="Chat with AI", description="Chat with AI")
async def chat(message: str):
    result = await llm.ainvoke(message)
    return {
        "message": result.content
    }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9527)