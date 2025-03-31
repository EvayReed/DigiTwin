from app.core.models.user import User
from app.core.utils.agent import get_records_by_user_id
from app.services.database_service import get_db


def create_user(user_id: int, name: str, avatar: str = None, email: str = None, token: str = None) -> User:
    with next(get_db()) as db:
        new_user = User(
            userId=user_id,
            name=name,
            avatar=avatar,
            email=email,
            token=token
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception as e:
            db.rollback()
            raise e


def get_user_by_id(user_id: int) -> User | None:
    with next(get_db()) as db:
        user = db.query(User).filter(User.userId == user_id).first()
        return user


def update_user_token(user_id: int, token: str) -> User:
    with next(get_db()) as db:
        user = db.query(User).filter(User.userId == user_id).first()
        if user:
            user.token = token
            user.name = "dingkai开饿了"
            db.commit()
            db.refresh(user)
            return user
        else:
            return None


def get_user_config(user_id: int, name: str, avatar: str = None, email: str = None, token: str = None) -> dict:
    user = get_user_by_id(user_id)

    if not user:
        user = create_user(user_id, name, avatar, email, token)
    else:
        if user.token != token:
            user = update_user_token(user_id, token)

    agents = get_records_by_user_id(user_id)

    return {
        "user_id": user.userId,
        "name": user.name,
        "avatar": user.avatar,
        "email": user.email,
        "token": user.token,
        "agents": agents
    }
