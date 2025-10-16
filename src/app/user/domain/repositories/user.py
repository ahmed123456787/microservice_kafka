from app.user.domain.entities.user import User
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_by_username(self, username: str) -> User:
        raise NotImplementedError
    
    @abstractmethod
    def update_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, username: str) -> None:
        raise NotImplementedError