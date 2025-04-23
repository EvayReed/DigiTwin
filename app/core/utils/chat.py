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

PROMPT_TEMPLATES = {
    "general": "你是一个专业的助手，请用中文回答用户的问题。",
    "document checklist": """####证件清单

        检索资源库中的用户证件，并按所属用户进行分类显示输出；
        ### 处理流程
        1. 数据检查阶段：
            - 执行资源库全量扫描
            - 严格区分「存在证件数据」与「空数据」两种状态

        2. 输出控制逻辑：
            如果资源库存在有效证件数据，执行「#输出-已上传」模块，禁止生成任何虚构或模拟的数据；
            如果资源库没有证件数据，执行「#输出-未上传」模块，禁止返回占位符或模拟信息；

        ### 格式规范
        - 结构： 
            - 直接以概述开头（除非用户要求特定标题）
            - 使用段落和简洁表格组织内容
            - 适量使用icon增强状态表现力
            - 结尾针对异常状态进行提醒与建议

        ###  输出-已上传
            1. - 概述：简要总结检索结果；
            2. - 清单：将证件按不同归属人进行分类
            - 分类后的证件用表格呈现，表格包括以下字段内容{证件名称，证件号，证件状态，证件说明}
            - 证件预警：提示{持证人},的证件出预警说明{如：时效性，合规性，多证件字段一致性等}
            3. -使用提醒 ：根据证件用途或状态，对{持证人},进行提醒或建议{如：护照免签国，驾照可用国家，相关证件地区性福利等}

        ###  输出-未上传
        响应模板：
        您好，目前尚未在您的数字保险库中发现任何证件信息。""",


    "Financial Digital Assistant": """  """,
    "insurance": "你是一个专业的保险顾问，请用中文回答用户的问题。",
    "retirement": "你是一个专业的退休规划顾问，请用中文回答用户的问题。"
}

async def stream_chat(query: str, type: str, ai_engine,user_id: str):
    """流式聊天核心逻辑"""
    try:
        llm = ai_engine.get_openai_model()
        system_prompt = PROMPT_TEMPLATES.get(type.lower(), PROMPT_TEMPLATES["general"])
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

        async def content_generator():
            stream = llm.astream(messages)
            async for chunk in stream:
                if chunk.content:
                    yield {
                        "data": {
                            "content": chunk.content,
                            "timestamp": datetime.now().isoformat(),
                            "query_type": type
                        }
                    }
                await asyncio.sleep(0)

        return content_generator()
    
    except Exception as e:
        logger.error(f"Stream chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))





