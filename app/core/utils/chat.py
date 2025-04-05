from datetime import datetime

from langchain.schema import HumanMessage, AIMessage
from app.core.models.chat import ChatMessage
from app.core.prompts.system import HINT
from app.services.database_service import get_db
from app.services.llm_service import ai_engine


def chat(query: str, chat_room_id: str) -> str:
    with next(get_db()) as session:
        llm = ai_engine.get_openai_model()
        try:
            user_msg = ChatMessage(
                chat_room_id=chat_room_id,
                role="user",
                content=query
            )
            session.add(user_msg)
            session.commit()

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
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            history.append(AIMessage(content=f"当前时间是: {current_time}"))
            response = llm(history)

            history.append(AIMessage(content=response.content))
            history.append(HumanMessage(content=HINT))
            hint_result = llm(history)
            print(hint_result.content)

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
