from pydantic import BaseModel

class UserSession(BaseModel):
    def __init__(self,user_id:int,token:str):
        self.user_id=user_id
        self.token=token

    