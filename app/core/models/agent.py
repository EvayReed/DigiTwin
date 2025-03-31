from xmlrpc.client import Boolean

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional

Base = declarative_base()


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String)
    personality = Column(String)
    avatar = Column(String)
    voice = Column(Integer)
    language = Column(String)
    has_welcome = Column(Integer)

    def __repr__(self):
        return f"<Agent(id={self.id}, user_id={self.user_id}, name={self.name})>"


class AgentCreateRequest(BaseModel):
    name: str
    avatar: str
    voice: Optional[int] = None
    language: Optional[str] = None
    personality: Optional[str] = None