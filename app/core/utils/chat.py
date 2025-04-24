import logging
from datetime import datetime
from typing import List
from langchain.schema import BaseMessage, HumanMessage, AIMessage, SystemMessage
from app.core.models.chat import ChatMessage
from app.core.prompts.credentials import credentials_tool_dict
from app.core.prompts.files import get_refer
from app.core.prompts.system import HINT, main_prompt
from app.core.tools.prompt_route import PromptRouterChain
from app.services.database_service import get_db
from app.services.llm_service import ai_engine
from app.services.vector_database_server import vector_db_man
from app.prompt.chat_stream_prompt import PROMPT_TEMPLATES
import asyncio
import logging
from fastapi import APIRouter, HTTPException, Request

logger = logging.getLogger(__name__)

def chat(query: str, chat_room_id: str) -> str:
    with next(get_db()) as session:
        llm = ai_engine.get_openai_model()
        try:
            past_msgs = session.query(ChatMessage) \
                .filter_by(chat_room_id=chat_room_id) \
                .order_by(ChatMessage.timestamp.desc()) \
                .limit(4) \
                .all()

            past_msgs.reverse()

            history = []
            for msg in past_msgs:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "ai":
                    history.append(AIMessage(content=msg.content))

            response = generateResponse(history, query)
            history.append(HumanMessage(content=query))
            history.append(AIMessage(content=response.get("content")))
            history.append(HumanMessage(content=HINT))
            hint_result = llm(history)
            print(hint_result.content)

            user_msg = ChatMessage(
                chat_room_id=chat_room_id,
                role="user",
                content=query
            )
            session.add(user_msg)
            ai_msg = ChatMessage(
                chat_room_id=chat_room_id,
                role="ai",
                content=response.get("content")
                # content=f"{response.get("refers")}{response.get("content")}"
            )
            session.add(ai_msg)
            session.commit()

            return {
                "result": response.get("content"),
                "hint": hint_result.content,
                "object": response
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class ToolResponse:
    def __init__(self, content: str):
        self.content = content


def append_context(context_texts=None):
    if not context_texts:
        return ""

    result = "\nContext:\n"
    for i, text in enumerate(context_texts):
        result += f"[CONTEXT {i}]:\n{text}\n[END CONTEXT {i}]\n\n"
    return result


def generateMonthlyLedger(history: List[BaseMessage], query: str, prompt: str) -> ToolResponse:
    llm = ai_engine.get_openai_model()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    refers = append_context(vector_db_man.query_knowledge_base(query, "sdm"))
    # refers = get_refer(query)
    logging.error(f"{query}查询到的相关信息：{refers}")
    # messages = [SystemMessage(content=f"此刻是{current_time}{main_prompt}{refers}")]
    messages = [SystemMessage(content=f"此刻是{current_time}{prompt}{refers}")]
    messages.extend(history)
    messages.append(HumanMessage(content=query))
    # history.append(HumanMessage(content=refers))
    # history.append(HumanMessage(content=prompt))
    # history.append(HumanMessage(content=f"{query}(此刻是{current_time})"))
    return {
        "content":  llm.invoke(messages).content,
        "refers": refers,
        "history": history
    }


def generateResponse(history: List[BaseMessage], query: str) -> ToolResponse:
    router_chain = PromptRouterChain(credentials_tool_dict)
    tool_info = router_chain.run(query)
    return generateMonthlyLedger(history, query, tool_info["selected_prompt"])

async def stream_chat(query: str, type: str, ai_engine,user_id: str):
    """流式聊天核心逻辑"""
    try:
        llm = ai_engine.get_openai_model()
        # 修改获取 system_prompt 的部分
        system_prompt = PROMPT_TEMPLATES.get(type, PROMPT_TEMPLATES.get("general", ""))
        with next(get_db()) as session:
            # 获取聊天记录
            chat_room_id = user_id
            past_msgs = session.query(ChatMessage) \
                .filter_by(chat_room_id=chat_room_id) \
                .order_by(ChatMessage.timestamp.desc()) \
                .limit(4) \
                .all()

            past_msgs.reverse()

            history = []
            for msg in past_msgs:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "ai":
                    history.append(AIMessage(content=msg.content))

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        refers = append_context(vector_db_man.query_knowledge_base(query, "sdm"))
        logging.error(f"{query}查询到的相关信息：{refers}")
        messages = [SystemMessage(content=f"此刻是{current_time}{system_prompt}{refers}")]
        messages.extend(history)
        messages.append(HumanMessage(content=query))
        # print(f'message{messages}')
        async def content_generator():
            # full_response 可以在最后返回整体回复，用于测试
            # full_response = ""
            stream = llm.astream(messages)
            async for chunk in stream:
                if chunk.content:
                    # full_response += chunk.content
                    yield {
                        "data": {
                            "content": chunk.content,
                            "timestamp": datetime.now().isoformat(),
                            "query_type": type
                        }
                    }
                await asyncio.sleep(0)
            # # 返回完整的输出
            # yield {
            #     "data": {
            #         "content": full_response,
            #         "timestamp": datetime.now().isoformat(),
            #         "query_type": type,
            #         "is_complete": True
            #     }
            # }

        return content_generator()
    
    except Exception as e:
        logger.error(f"Stream chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))





