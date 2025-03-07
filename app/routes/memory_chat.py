import uuid
from datetime import datetime
from typing import Dict

from fastapi import APIRouter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from starlette.websockets import WebSocketDisconnect
from starlette.websockets import WebSocket
from langchain_community.chat_message_histories import SQLChatMessageHistory
from app.services.memory_service import RunnableHistoryMemory
from app.services.llm_service import ai_engine

router = APIRouter(tags=["memory_Chat"])

memory = RunnableHistoryMemory(
    ai_engine.get_chat_model()
)

@router.post("/chat_memory",
             summary="Chat with memory",
             description="memory chat")
async def chat(message: str):
    try:
        response = memory.process_input(message)
        return {
            "state": 200,
            "message": response.content,
        }
    except Exception as e:
        return {
            "state": 500,
            "error": str(e),
        }


# @router.websocket("/chat_memory/wsChat")
# async def websocket_endpoint(websocket: WebSocket):
#     wsChat_memory = RunnableHistoryMemory(
#         engine.get_llm(),
#     )
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             response = await wsChat_memory.process_input(data)
#             await websocket.send_text(response)
#     except WebSocketDisconnect:
#         print("Client disconnected")
#         await websocket.close()

# @router.websocket("/chat_memory_wsChat")
# async def websocket_endpoint(websocket: WebSocket):
#     # 新增会话ID获取逻辑
#     session_id = websocket.query_params.get("session_id") or str(uuid.uuid4())
#     # 改造记忆初始化（从存储加载历史）
#     wsChat_memory = RunnableHistoryMemory(
#         ai_engine.get_llm(),
#         session_id=session_id
#     )
#
#     await websocket.accept()
#     try:
#         await websocket.send_text(f"SESSION_ID:{session_id}")  # 告知客户端会话ID
#         while True:
#             data = await websocket.receive_text()
#             response = await wsChat_memory.process_input(data, history=wsChat_memory.load_history())
#             await websocket.send_text(response)
#     except WebSocketDisconnect:
#         print(f"Session {session_id} disconnected")
#     except Exception as e:
#         await websocket.send_text(f"ERROR:{str(e)}")

# @router.websocket("/chat_memory_wsChat")
# async def websocket(websocket: WebSocket):
#     await websocket.accept()
#     await websocket.send_json({"msg": "Hello WebSocket"})
#     await websocket.close()

# 存储活跃会话（可选）
active_sessions: Dict[str, WebSocket] = {}


@router.websocket("/chat_memory_wsChat")
async def websocket_chat(websocket: WebSocket):
    # 建立连接
    await websocket.accept()

    # 生成唯一会话ID
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = websocket  # 记录会话
    wsChat_memory = RunnableHistoryMemory(
        ai_engine.get_chat_model(),
        session_id=session_id
    )

    try:
        # 发送连接确认
        await websocket.send_json({
            "status": "connected",
            "session_id": session_id,
            "instruction": "输入 'exit' 结束会话"
        })

        # 消息处理循环
        while True:
            # 接收客户端消息（支持文本/JSON）
            message = await websocket.receive_json()

            # 处理退出指令
            if message.get("content") == "exit":
                await websocket.send_json({"status": "disconnecting"})
                break

            # 业务处理逻辑
            response = wsChat_memory.process_input(message.get("content"))

            # 发送响应
            await websocket.send_json(response.content)

    except WebSocketDisconnect:
        print(f"会话 {session_id} 客户端主动断开")
    except Exception as e:
        await websocket.send_json({
            "status": "error",
            "detail": str(e)
        })
    finally:
        # 清理会话资源
        await websocket.close()
        active_sessions.pop(session_id, None)
        print(f"会话 {session_id} 已释放")


async def process_message(message: dict) -> dict:
    """消息处理核心逻辑"""
    # 示例：添加时间戳并反转消息内容
    return {
        "timestamp": datetime.now().isoformat(),
        "original": message.get("content", ""),
        "processed": message.get("content", "")[::-1]
    }

