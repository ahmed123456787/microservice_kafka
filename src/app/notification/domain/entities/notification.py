from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

class NotificationStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"

#########################################################################################

class Notification(ABC):
    """Base notification entity"""
    
    def __init__(self, message: str):
        self.id = None  # Set by repository
        self.message = message
        self.status = NotificationStatus.PENDING
        self.created_at = datetime.now()
        self.sent_at = None
        self.error_message = None
    
    def mark_as_sent(self):
        if self.status != NotificationStatus.PENDING:
            raise ValueError(f"Cannot mark as sent. Current status: {self.status}")
        self.status = NotificationStatus.SENT
        self.sent_at = datetime.now()
    
    def mark_as_failed(self, error_message: str):
        self.status = NotificationStatus.FAILED
        self.error_message = error_message
    
    @abstractmethod
    def is_valid(self) -> bool:
        """Validate notification according to type-specific rules"""
        pass
    
    @abstractmethod
    def get_recipient(self) -> str:
        """Get the recipient identifier"""
        pass
    
    @abstractmethod
    def get_type(self) -> str:
        """Get notification type name"""
        pass

#########################################################################################

class EmailNotification(Notification):
    def __init__(self, message: str, email: str, subject: str, cc: list = None):
        super().__init__(message)
        self.email = email
        self.subject = subject
        self.cc = cc or []
    
    def is_valid(self) -> bool:
        return (
            bool(self.email and self.subject and self.message) and
            "@" in self.email and
            "." in self.email.split("@")[1]
        )
    
    def get_recipient(self) -> str:
        return self.email
    
    def get_type(self) -> str:
        return "EMAIL"
    
#########################################################################################

class SMSNotification(Notification):
    MAX_LENGTH = 160
    
    def __init__(self, message: str, phone_number: str):
        super().__init__(message)
        self.phone_number = phone_number
    
    def is_valid(self) -> bool:
        return (
            bool(self.phone_number and self.message) and
            len(self.message) <= self.MAX_LENGTH and
            self.phone_number.startswith("+")
        )
    
    def get_recipient(self) -> str:
        return self.phone_number
    
    def get_type(self) -> str:
        return "SMS"

#########################################################################################

class PushNotification(Notification):
    def __init__(self, message: str, device_token: str, title: str, data: dict = None):
        super().__init__(message)
        self.device_token = device_token
        self.title = title
        self.data = data or {}
    
    def is_valid(self) -> bool:
        return bool(self.device_token and self.message and self.title)
    
    def get_recipient(self) -> str:
        return self.device_token
    
    def get_type(self) -> str:
        return "PUSH"