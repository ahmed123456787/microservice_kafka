from domain.ports.notification_port import NotificationPort
from domain.entities.notification import Notification

class NotificationService:

    @staticmethod
    def send_notification(notification_port: NotificationPort, notification:Notification) -> bool:
        notification_port.send(notification)