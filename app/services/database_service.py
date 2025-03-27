from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 定义 User 模型
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer, index=True)


# 查询所有数据
def get_all_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Username: {user.name}, Email: {user.age}")
    finally:
        session.close()


# 调用函数查询
get_all_users()