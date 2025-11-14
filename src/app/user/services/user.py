from typing import  Dict, Any
from sqlalchemy.orm import Session
from models import User as DbUser
from .base_service_crud import BaseService

# call the producer.
from producer import produce_message
from .validators import validate_user_uniqueness

class UserService(BaseService):
    def __init__(self, session: Session):
        super().__init__(DbUser, session)

    def _to_response_dict(self, user: DbUser) -> Dict[str, Any]:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "age": user.age,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "is_verified": user.is_verified,
        }

    async def create(self, **user_data) -> Dict[str, Any]:
        validate_user_uniqueness(self.session, user_data)

        user_data.setdefault("is_active", True)
        user_data.setdefault("is_superuser", False)
        user_data.setdefault("is_verified", False)

        new_user = await super().create(**user_data)
        print(new_user, " user")

        produce_message(
            topic="notification",
            key="user_created",
            value={
                "user_id": new_user["id"],
                "username": new_user["username"],
                "email": new_user["email"],
            }
        )

        return new_user


    def update(self, user_id: int, **update_data) -> Dict[str, Any]:
        validate_user_uniqueness(self.session, update_data, user_id=user_id)
        return super().update(user_id, **update_data)