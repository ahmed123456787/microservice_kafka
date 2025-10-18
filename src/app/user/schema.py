from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from .domain.enum.role import Role


class LoginRequest(BaseModel):
    """Login credentials validation"""
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class UserCreateRequest(BaseModel):
    """API input validation - format and basic constraints"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    role: Role
    age: Optional[int] = Field(None, ge=13, le=120)
    full_name: Optional[str] = Field(None, max_length=100)
    

    @field_validator('username')
    def username_format(cls, v):
        """API-level format validation"""
        if v.startswith(('admin', 'system')):
            raise ValueError('Username cannot start with reserved words')
        return v.lower()
    

    @field_validator('password')
    def password_format(cls, v):
        """Basic password format validation"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain a number')
        return v


class UserUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=13, le=120)
    full_name: Optional[str] = Field(None, max_length=100)



class UserResponse(BaseModel):
    """API output model"""
    id: int
    username: str
    email: EmailStr
    role: Role
    age: Optional[int]
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True