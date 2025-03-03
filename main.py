from fastapi import FastAPI
from app.routes import health, chat, files

app = FastAPI(
    title="DigiTwin Service API",
    version="1.0",
    description="LangChain API Deployment"
)

app.include_router(health.router)
app.include_router(chat.router)
app.include_router(files.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9527)