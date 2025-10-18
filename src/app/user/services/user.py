from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from models import User as DbUser
from domain.exception import UserNotFoundError

class UserService:
    def __init__(self, session: Session):
        self.session = session
    
    def _to_response_dict(self, db_user: DbUser) -> Dict[str, Any]:
        """Convert database model to response dictionary"""
        return {
            "id": db_user.id,
            "username": db_user.username,
            "email": db_user.email,
            "role": db_user.role,
            "age": db_user.age,
            "full_name": db_user.full_name,
            "is_active": db_user.is_active,
            "is_superuser": db_user.is_superuser,
            "is_verified": db_user.is_verified
        }
    
    def get_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID and return response dictionary"""
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if not db_user:
            raise UserNotFoundError(f"{user_id}")
        return self._to_response_dict(db_user)
    
    def create(self, **user_data) -> Dict[str, Any]:
        """Create a user using keyword arguments and return response dictionary"""
        # Add validation for uniqueness
        existing_user = self.session.query(DbUser).filter(
            DbUser.username == user_data.get('username')
        ).first()
        if existing_user:
            raise ValueError("Username already exists")
        
        existing_email = self.session.query(DbUser).filter(
            DbUser.email == user_data.get('email')
        ).first()
        if existing_email:
            raise ValueError("Email already exists")
        
        # Set default values for required fields
        user_data.setdefault('is_active', True)
        user_data.setdefault('is_superuser', False)
        user_data.setdefault('is_verified', False)
        
        # Create DB model
        db_user = DbUser(**user_data)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return self._to_response_dict(db_user)
    
    def update(self, user_id: int, **update_data) -> Optional[Dict[str, Any]]:
        """Update a user with the provided data and return response dictionary"""
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if not db_user:
            return None
        
        # Check uniqueness for updated fields
        if 'username' in update_data:
            existing = self.session.query(DbUser).filter(
                DbUser.username == update_data['username'],
                DbUser.id != user_id
            ).first()
            if existing:
                raise ValueError("Username already exists")
        
        if 'email' in update_data:
            existing = self.session.query(DbUser).filter(
                DbUser.email == update_data['email'],
                DbUser.id != user_id
            ).first()
            if existing:
                raise ValueError("Email already exists")
            
        # Update only the fields provided
        for key, value in update_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
                
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_response_dict(db_user)
    
    def delete(self, user_id: int) -> bool:
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
            return True
        return False
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all users and return list of response dictionaries"""
        db_users = self.session.query(DbUser).all()
        return [self._to_response_dict(user) for user in db_users]