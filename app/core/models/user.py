from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'  # 表的名称

    # 定义表的列
    id = Column(Integer, primary_key=True, index=True)  # 主键
    userId = Column(Integer, nullable=False)  # 用户 ID
    name = Column(String(255), nullable=False)  # 用户名
    avatar = Column(String(255), nullable=True)  # 头像 URL
    email = Column(String(255), unique=True, nullable=False)  # 唯一的邮箱
    token = Column(String(255), unique=True, nullable=False)  # 唯一的token

    def __repr__(self):
        return f"<User(id={self.id}, userId={self.userId}, name={self.name}, email={self.email}), token={self.token})>"
