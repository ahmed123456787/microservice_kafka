from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..services.user import UserService
from ..services.session import UserSessionService
from ..domain.entities.user import User as DomainUser
from ..domain.exception import UserNotFoundError
from ..schema import UserCreateRequest, UserUpdateRequest, UserResponse, LoginRequest

from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


# Dependency to get UserService
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# Dependency to get SessionService
def get_session_service(db: Session = Depends(get_db)) -> UserSessionService:
    return UserSessionService(db)

@router.get("/", response_model=List[UserResponse])
async def get_all_users(user_service: UserService = Depends(get_user_service)):
    """Get all users"""
    return user_service.get_all()



@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    """Get a user by ID"""
    try:
        user = user_service.get_by_id(user_id)
        return user
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
 



@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreateRequest,  # Use Pydantic validator instead of DomainUser
    user_service: UserService = Depends(get_user_service)
):
    """Create a new user"""
    try:
        user_dict = user_data.model_dump()  # This triggers Pydantic validation
        
        # Service handles business validation
        user = user_service.create(**user_dict)
        return user 
    except ValueError as e:  # Service validation errors
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int, 
    update_data: UserUpdateRequest,  # Use Pydantic validator instead of dict
    user_service: UserService = Depends(get_user_service)
):
    """Update a user"""
    try:
        # Convert to dict and filter out None values
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        
        updated_user = user_service.update(user_id, **update_dict)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return updated_user
        
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")



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
    credentials: LoginRequest,  # Use Pydantic validator instead of dict
    user_service: UserService = Depends(get_user_service),
    session_service: UserSessionService = Depends(get_session_service)
):
    """Login a user and create a session"""
    try:
        # Authentication logic would go here
        # For now, placeholder
        user_id = 1  # Replace with actual user ID from authentication
        
        # Create a session token
        token = session_service.create_session(user_id)
        
        return {"token": token}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")