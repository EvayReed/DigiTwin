from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"))


def get_db():
    db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()
    try:
        yield db_session
    finally:
        db_session.close()
