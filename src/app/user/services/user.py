from typing import List, Optional
from sqlalchemy.orm import Session
from domain.entities.user import User as DomainUser
from schema import User as DbUser
from domain.exception import UserNotFoundError

class UserService:
    def __init__(self, session: Session):
        self.session = session
    
    def _to_domain(self, db_user: DbUser) -> DomainUser:
        """Convert database model to domain entity"""
        return DomainUser(**db_user)
    
    def _to_db(self, domain_user: DomainUser) -> DbUser:
        """Convert domain entity to database model"""
        # Extract all attributes from domain user that match the DB model
        user_dict = {
            attr: getattr(domain_user, attr)
            for attr in ['id', 'username', 'email', 'role', 'password', 'age', 
                         'is_active', 'is_superuser', 'is_verified', 'full_name']
            if hasattr(domain_user, attr)
        }
        return DbUser(**user_dict)
    
    def get_by_id(self, user_id: int) -> Optional[DomainUser]:
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if not db_user:
            return UserNotFoundError(f"User with id '{user_id}' not found.")
        return self._to_domain(db_user)
    
    def create(self, **user_data) -> DomainUser:
        """Create a user using keyword arguments"""
        # First create domain entity to ensure domain validation
        domain_user = DomainUser(**user_data)
        
        # Then create DB model
        db_user = DbUser(**user_data)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        
        return self._to_domain(db_user)
    
    def update(self, user_id: int, **update_data) -> Optional[DomainUser]:
        """Update a user with the provided data"""
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if not db_user:
            return None
            
        # Update only the fields provided
        for key, value in update_data.items():
            if hasattr(db_user, key):
                setattr(db_user, key, value)
                
        self.session.commit()
        self.session.refresh(db_user)
        return self._to_domain(db_user)
    
    def delete(self, user_id: int) -> bool:
        db_user = self.session.query(DbUser).filter(DbUser.id == user_id).first()
        if db_user:
            self.session.delete(db_user)
            self.session.commit()
            return True
        return False
    
    def get_all(self) -> List[DomainUser]:
        db_users = self.session.query(DbUser).all()
        return [self._to_domain(user) for user in db_users]