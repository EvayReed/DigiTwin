from fastapi import FastAPI
from app.routes import health, chat, files, audio, login, agent

app = FastAPI(
    title="DigiTwin Service API",
    version="1.0",
    description="LangChain API Deployment"
)

app.include_router(health.router)
app.include_router(login.router)
app.include_router(chat.router)
app.include_router(files.router)
app.include_router(audio.router)
app.include_router(agent.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9527)
