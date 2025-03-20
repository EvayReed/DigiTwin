from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.services.database_service import Base


class ChatRecord(Base):
    __tablename__ = 'chat_records'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自增主键
    conversation_id = Column(String(255), nullable=False)       # 对话框 ID
    message = Column(Text, nullable=False)                       # 消息内容
    timestamp = Column(DateTime, nullable=False)                 # 消息时间
    from_user = Column(String(255), nullable=False)              # 发送者
    to_user = Column(String(255), nullable=False)                # 接收者