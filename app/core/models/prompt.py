from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Prompt(Base):
    __tablename__ = 'prompts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String(20), unique=True, nullable=False)
    type = Column(String(20), nullable=False)
    prompt = Column(Text, nullable=False)
