from app.core.models.chat_records import ChatRecord
from app.services.database_service import SessionLocal


def get_chat_records_by_conversation(conversation_id: str):
    db = SessionLocal()
    result = db.query(ChatRecord).filter(ChatRecord.conversation_id == conversation_id).all()
    db.close()
    return result


def get_chat_records_by_user(from_user: str, to_user: str):
    db = SessionLocal()
    result = db.query(ChatRecord).filter(ChatRecord.from_user == from_user, ChatRecord.to_user == to_user).all()
    db.close()
    return result
