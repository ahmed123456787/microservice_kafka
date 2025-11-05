from sqlalchemy.orm import Session
from models import User as DbUser

def validate_user_uniqueness(session: Session, data: dict, user_id: int = None):
    """
    Validates the uniqueness of username and email.
    Raises ValueError if a value is not unique.
    """
    username = data.get("username")
    if username:
        query = session.query(DbUser).filter(DbUser.username == username)
        if user_id:
            query = query.filter(DbUser.id != user_id)
        if query.first():
            raise ValueError("Username already exists")

    email = data.get("email")
    if email:
        query = session.query(DbUser).filter(DbUser.email == email)
        if user_id:
            query = query.filter(DbUser.id != user_id)
        if query.first():
            raise ValueError("Email already exists")