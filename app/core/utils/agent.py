from app.core.models.agent import Agent
from app.services.database_service import get_db


def add_agent(
    user_id: str, name: str,
    avatar: str, voice: int = None, language: str = None,
    personality: str = None
):
    with next(get_db()) as db:
        try:
            new_agent = Agent(
                user_id=user_id,
                name=name,
                avatar=avatar,
                voice=voice,
                language=language,
                personality=personality,
                has_welcome=0
            )
            db.add(new_agent)
            db.commit()
            db.refresh(new_agent)
            print("Record added successfully.")
            return new_agent
        except Exception as e:
            db.rollback()
            print(f"Error: {e}")
            return None


def get_agents_by_user_id(user_id: str):
    with next(get_db()) as db:
        try:
            records = db.query(Agent).filter(Agent.user_id == user_id).all()
            return records
        except Exception as e:
            print(f"Error: {e}")
            return []
