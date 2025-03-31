from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Agent(Base):
    __tablename__ = 'agents'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    name = Column(String)
    character = Column(String)
    profession = Column(String)
    avatar = Column(String)

    def __repr__(self):
        return f"<Agent(id={self.id}, user_id={self.user_id}, name={self.name})>"
