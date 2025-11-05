from typing import List, Dict, Any, Optional, Type
from sqlalchemy.orm import Session

class BaseService:
    def __init__(self, model: Type, session: Session):
        self.model = model
        self.session = session

    def _to_response_dict(self, obj) -> Dict[str, Any]:
        """Convert DB instance to dict (override in child if needed)."""
        return {column.name: getattr(obj, column.name) for column in self.model.__table__.columns}

    def get_by_id(self, obj_id: int) -> Dict[str, Any]:
        db_obj = self.session.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            raise ValueError(f"{self.model.__name__} {obj_id} not found")
        return self._to_response_dict(db_obj)

    def get_all(self) -> List[Dict[str, Any]]:
        objs = self.session.query(self.model).all()
        return [self._to_response_dict(obj) for obj in objs]

    async def create(self, **data) -> Dict[str, Any]:
        db_obj = self.model(**data)
        self.session.add(db_obj)
        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_response_dict(db_obj)

    def update(self, obj_id: int, **data) -> Optional[Dict[str, Any]]:
        db_obj = self.session.query(self.model).filter(self.model.id == obj_id).first()
        if not db_obj:
            return None

        for key, value in data.items():
            if hasattr(db_obj, key):
                setattr(db_obj, key, value)

        self.session.commit()
        self.session.refresh(db_obj)
        return self._to_response_dict(db_obj)

    def delete(self, obj_id: int) -> bool:
        db_obj = self.session.query(self.model).filter(self.model.id == obj_id).first()
        if db_obj:
            self.session.delete(db_obj)
            self.session.commit()
            return True
        return False
