from typing import Any, Dict
import logging
from services.notification_service import NotificationService
from models import Notification
from datetime import datetime

from .event import UserCreatedEvent
from .base_consumer import AsyncEventConsumer

logger = logging.getLogger(__name__)


class UserEventConsumer(AsyncEventConsumer):
    """Handle user events"""

    async def process_event(self, event_data: Dict[str, Any]):
        logger.info(f"📨 Event received: {event_data}")

        if not all(field in event_data for field in ("user_id", "username", "email")):
            logger.warning(f"⚠️ Invalid event format: {event_data}")
            return

        event = UserCreatedEvent(**event_data)
        await self._on_user_created(event)


    async def _on_user_created(self, event: UserCreatedEvent):
        logger.info(f"👤 User created: {event.username} | {event.email}")
        await NotificationService.create(
            db_obj=Notification(
                notification_type="SMS",
                user_id=event.user_id,
                message=f"Welcome {event.username}! Your account has been created.",
                is_read=False,
                created_at=datetime.now()
            ),
        )