from sqlalchemy.exc import IntegrityError
from app.core.models.prompt import Prompt
from app.services.database_service import get_db


def add_or_update_entry(tag, prompt_type, prompt):
    with next(get_db()) as session:
        existing_entry = session.query(Prompt).filter_by(tag=tag).first()

        if existing_entry:
            existing_entry.type = prompt_type
            existing_entry.prompt = prompt
        else:
            existing_entry = Prompt(tag=tag, type=prompt_type, prompt=prompt)
            session.add(existing_entry)

        try:
            session.commit()
            return existing_entry
        except IntegrityError as e:
            session.rollback()
            raise e
