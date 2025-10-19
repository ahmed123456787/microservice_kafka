from enum.not_type import NotificationType

class Notification:
    def __init__(self, id: int, user_id: int, message: str, created_at: str, 
                 notf_type: NotificationType, is_read: bool = False):
        self.id = id
        self.user_id = user_id
        self.message = message
        self.created_at = created_at
        self.is_read = False
        self.type = notf_type
    
    def mark_as_read(self):
        self.is_read = True


