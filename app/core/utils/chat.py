import logging
from datetime import datetime
from typing import List
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from app.core.models.chat import ChatMessage
from app.core.prompts.credentials import credentials_tool_dict
from app.core.prompts.system import HINT
from app.core.tools.prompt_route import PromptRouterChain
from app.services.database_service import get_db
from app.services.llm_service import ai_engine
from app.services.vector_database_server import vector_db_man


def chat(query: str, chat_room_id: str) -> str:
    with next(get_db()) as session:
        llm = ai_engine.get_openai_model()
        try:
            past_msgs = session.query(ChatMessage) \
                .filter_by(chat_room_id=chat_room_id) \
                .order_by(ChatMessage.timestamp.desc()) \
                .limit(10) \
                .all()

            past_msgs.reverse()

            history = []
            for msg in past_msgs:
                if msg.role == "user":
                    history.append(HumanMessage(content=msg.content))
                elif msg.role == "ai":
                    history.append(AIMessage(content=msg.content))

            response = generateResponse(history, query)
            print(response)

            history.append(HumanMessage(content=query))
            history.append(AIMessage(content=response.content))
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
                content=response.content
            )
            session.add(ai_msg)
            session.commit()

            return {
                "result": response.content,
                "hint": hint_result.content
            }

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class ToolResponse:
    def __init__(self, content: str):
        self.content = content


def generateMonthlyLedger(history: List[BaseMessage], query: str, prompt: str) -> ToolResponse:
    llm = ai_engine.get_openai_model()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    refers = ";".join(vector_db_man.query_knowledge_base(query, "sdm"))
    logging.error(f"{query}查询到的相关信息：{refers}")
    history.append(HumanMessage(content=refers))
    history.append(HumanMessage(content=prompt))
    history.append(HumanMessage(content=f"{query}(此刻是{current_time})"))
    return llm.invoke(history)


def generateResponse(history: List[BaseMessage], query: str) -> ToolResponse:
    router_chain = PromptRouterChain(credentials_tool_dict)
    tool_info = router_chain.run(query)
    return generateMonthlyLedger(history, query, tool_info["selected_prompt"])





