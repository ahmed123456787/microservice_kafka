from pydantic import BaseModel
from typing import Any, Dict
from datetime import datetime

class KafkaEvent(BaseModel):
    event_type: str
    event_id: str
    timestamp: datetime



class UserCreatedEvent(BaseModel):
    user_id: int    
    username: str
    email: str
