from sqlalchemy.orm import Session
from domain.entities.session import UserSession
from domain.repositories.session import SessionRepository


class UserSessionService(SessionRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_session(self, user_id: int) -> str:
        new_session = UserSession(user_id=user_id)
        self.db_session.add(new_session)
        self.db_session.commit()
        self.db_session.refresh(new_session)
        return new_session.token

    def get_user_id_by_token(self, token: str) -> int:
        session = self.db_session.query(UserSession).filter(UserSession.token == token).first()
        if not session:
            raise ValueError("Invalid session token")
        return session.user_id