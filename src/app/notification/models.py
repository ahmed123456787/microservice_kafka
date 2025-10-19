from database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime,Enum
from datetime import datetime
from domain.enum.not_type import NotificationType


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    message = Column(String, index=True)
    notification_type = Column(Enum(NotificationType), nullable=False,default=NotificationType.EMAIL)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.time)