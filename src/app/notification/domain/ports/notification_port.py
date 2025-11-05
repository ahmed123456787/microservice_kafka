from abc import ABC, abstractmethod
from ..entities.notification import Notification

class NotificationPort(ABC):

    @abstractmethod
    def send(self, notification:Notification) -> bool:
        """Send a notification"""
        pass