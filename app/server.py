from fastapi import FastAPI
from langchain.prompts import ChatPromptTemplate
from langserve import add_routes
from langchain_ollama import ChatOllama

app = FastAPI(
    title="AI Service API",
    version="1.0",
    description="LangChain API Deployment"
)

# 基础模型路由
llm = ChatOllama(
    model="deepseek-r1:1.5b",
    temperature=0.7,
    base_url="http://localhost:11434"
)

@app.get("/health")
async def service_healthcheck():
    """服务健康状态监测接口"""
    return {
        "status": "active",
        "timestamp": 23424,
        "service": "LangChain API v1.0"
    }

from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    user_question: str = Field(...,
                              min_length=5,
                              max_length=500,
                              description="用户提问内容，5-500字符")
    temperature: float = Field(0.7,
                              ge=0.0,
                              le=1.0,
                              description="生成文本的随机性控制参数")

@app.post("/ask-question",
          response_model=dict,
          summary="问题处理接口",
          description="接收用户提问并调用语言模型生成回答")
async def process_question(request: QuestionRequest):
    # 调用语言模型生成响应
    model_response = await llm.ainvoke(
        f"用户提问：{request.user_question}\n系统回答："
    )

    return {
        "original_question": request.user_question,
        "model_response": model_response.content,
        "temperature": request.temperature,
        "processing_time": f"{1231231}"
    }

class QueryRequest(BaseModel):
    user_input: str
    max_length: int = 100

@app.post("/text-process")
async def custom_text_processing(request: QueryRequest):
    processed_text = f"处理结果：{request.user_input[:request.max_length]}"
    return {
        "original_input": request.user_input,
        "processed_result": processed_text,
        "character_count": len(processed_text)
    }

add_routes(app, llm, path="/chat")

# 组合式服务路由
prompt = ChatPromptTemplate.from_template("分析主题：{topic}")
chain = prompt | llm
add_routes(app, chain, path="/analyze")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4399)