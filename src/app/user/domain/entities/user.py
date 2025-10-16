from typing import Optional
from domain.enum.role import Role
from pydantic import BaseModel

class User(BaseModel):
    def __init__(self,
                 id: int,
                 username: str,
                 email: str,
                 role: Role,
                 password: str ,
                 age: Optional[int] = None,
                 is_active: bool = True,
                 is_superuser: bool = False,
                 is_verified: bool = False,
                 full_name: Optional[str] = None):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.age = age
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.is_verified = is_verified
        self.full_name = full_name
        

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role.name}', age={self.age}, is_active={self.is_active}, is_superuser={self.is_superuser}, is_verified={self.is_verified}, full_name='{self.full_name}')"