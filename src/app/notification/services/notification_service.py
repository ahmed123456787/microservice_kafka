from domain.ports.notification_port import NotificationPort
from sqlalchemy.orm import Session
from models import Notification
from database import get_db, SessionLocal
from fastapi import Depends

class NotificationService:

    @staticmethod
    def send_notification(notification_port: NotificationPort, notification:Notification) -> bool:
        notification_port.send(notification)


    @staticmethod
    async def create(db_obj: Notification) -> bool:
        print("create the notification object")
        session = SessionLocal()
        try:
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
        finally:
            session.close()
        return True