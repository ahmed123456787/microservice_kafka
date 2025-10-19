from domain.ports.notification_port import NotificationPort
from domain.entities.notification import EmailNotification, SMSNotification, PushNotification
from config.config import AppConfig

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class EmailNotificationAdapter(NotificationPort):
    
    def send(self, notification: EmailNotification) -> bool:
        if not notification.is_valid():
            return False
        
        # Logic for sending emails 
        def send_email_via_sendgrid(to_email, subject, content):
            message = Mail(
                from_email="your_email@example.com",
                to_emails=to_email,
                subject=subject,
                plain_text_content=content,
            )
            try:
                sg = SendGridAPIClient(AppConfig.SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
            except Exception as e:
                print(f"Error: {e}")

        send_email_via_sendgrid(notification.get_recipient(), notification.subject, notification.message)
        print(f"Sending Email to {notification.get_recipient()}: {notification.message}")
        return True
    


class SMSNotificationAdapter(NotificationPort):
    
    def send(self, notification: SMSNotification) -> bool:
        if not notification.is_valid():
            return False
        # Implement SMS sending logic here
        print(f"Sending SMS to {notification.get_recipient()}: {notification.message}")
        return True