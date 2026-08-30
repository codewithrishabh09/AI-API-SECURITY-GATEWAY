from sqlalchemy.orm import Session
from app.models.api_key import APIKey
import logging

logger = logging.getLogger(__name__)

class APIKeyRepository:
    """Repository for APIKey model"""
    
    @staticmethod
    def create(db: Session, api_key: str, project_id: int, name: str) -> APIKey:
        """Create new API key"""
        db_api_key = APIKey(
            key=api_key,
            project_id=project_id,
            name=name
        )
        db.add(db_api_key)
        db.commit()
        db.refresh(db_api_key)
        logger.info(f"API key created for project: {project_id}")
        return db_api_key
    
    @staticmethod
    def get_by_key(db: Session, key: str) -> APIKey:
        """Get API key by key value"""
        return db.query(APIKey).filter(APIKey.key == key).first()
    
    @staticmethod
    def get_by_id(db: Session, key_id: int) -> APIKey:
        """Get API key by ID"""
        return db.query(APIKey).filter(APIKey.id == key_id).first()
    
    @staticmethod
    def get_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
        """Get API keys by project"""
        return db.query(APIKey).filter(
            APIKey.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def revoke(db: Session, key_id: int) -> APIKey:
        """Revoke API key"""
        api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
        if api_key:
            api_key.is_active = False
            db.commit()
            db.refresh(api_key)
            logger.info(f"API key revoked: {api_key.key}")
        return api_key
    
    @staticmethod
    def delete(db: Session, key_id: int) -> bool:
        """Delete API key"""
        api_key = db.query(APIKey).filter(APIKey.id == key_id).first()
        if api_key:
            db.delete(api_key)
            db.commit()
            logger.info(f"API key deleted: {api_key.key}")
            return True
        return False