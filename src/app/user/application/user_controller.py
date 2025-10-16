from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from services.user import UserService
from services.session import UserSessionService
from domain.entities.user import User as DomainUser
from domain.exception import UserNotFoundError

# You'll need to import your database session dependency
from database import get_db

router = APIRouter(prefix="/users", tags=["users"])

# Dependency to get UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# Dependency to get SessionService
def get_session_service(db: Session = Depends(get_db)) -> UserSessionService:
    return UserSessionService(db)

@router.get("/", response_model=List[DomainUser])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """Get all users"""
    return user_service.get_all()

@router.get("/{user_id}", response_model=DomainUser)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Get a user by ID"""
    try:
        user = user_service.get_by_id(user_id)
        if isinstance(user, UserNotFoundError):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(user))
        return user
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/", response_model=DomainUser, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: dict, user_service: UserService = Depends(get_user_service)):
    """Create a new user"""
    try:
        return user_service.create(**user_data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}", response_model=DomainUser)
async def update_user(
    user_id: int, 
    update_data: dict,
    user_service: UserService = Depends(get_user_service)
):
    """Update a user"""
    updated_user = user_service.update(user_id, **update_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return updated_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Delete a user"""
    success = user_service.delete(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return None

@router.post("/login")
async def login_user(
    credentials: dict,  # You should define a proper Pydantic model for this
    user_service: UserService = Depends(get_user_service),
    session_service: UserSessionService = Depends(get_session_service)
):
    """Login a user and create a session"""
    # This is a placeholder - you'll need to implement authentication logic
    # For example, verifying username/password
    
    # Assuming authentication is successful and you have the user's ID
    user_id = 1  # Replace with actual user ID from authentication
    
    # Create a session token
    token = session_service.create_session(user_id)
    
    return {"token": token}