from app.core.models.agent import Agent
from app.services.database_service import get_db


def add_record(user_id: str, name: str, character: str, profession: str, avatar: str):
    with next(get_db()) as db:
        try:
            new_agent = Agent(
                user_id=user_id,
                name=name,
                character=character,
                profession=profession,
                avatar=avatar
            )
            db.add(new_agent)
            db.commit()
            db.refresh(new_agent)
            print("Record added successfully.")
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")


def get_records_by_user_id(user_id: str):
    with next(get_db()) as db:
        try:
            records = db.query(Agent).filter(Agent.user_id == user_id).all()
            return records
        except Exception as e:
            print(f"Error: {e}")
            return []
