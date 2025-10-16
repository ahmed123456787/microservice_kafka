
class SessionRepository:
    def create_session(self, user_id: int) -> str:
        raise NotImplementedError

    def get_user_id_by_token(self, token: str) -> int:
        raise NotImplementedError