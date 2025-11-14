from pydantic_settings import BaseSettings as PydanticBaseSettings
from dotenv import load_dotenv
import os
from domain.entities.service import Service

#Load environment variables from .env file
load_dotenv('../.env')


class BaseSettings(PydanticBaseSettings):
    env: str = os.getenv("ENV", "development")
    api_gateway_url: str = "http://localhost:8000"

    # They will change and I use service discovery in future
    user_service_url: str = "http://localhost:8001"
    notification_service_url: str = "http://localhost:8002"
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", "60"))



    @property
    def service_mapping(self) -> dict[str, Service]:
        return {
            "user": Service(
                name="user_service",
                url=self.user_service_url,
                slag="users"
            ),
            "notification": Service(
                name="notification_service",
                url=self.notification_service_url,
                slag="notifications"
            ),
        }
