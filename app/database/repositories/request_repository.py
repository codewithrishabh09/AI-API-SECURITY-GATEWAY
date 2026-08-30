from sqlalchemy.orm import Session
from app.models.request import Request
import logging

logger = logging.getLogger(__name__)

class RequestRepository:
    """Repository for Request model"""
    
    @staticmethod
    def create(db: Session, request_data: dict) -> Request:
        """Create new request record"""
        db_request = Request(**request_data)
        db.add(db_request)
        db.commit()
        db.refresh(db_request)
        logger.info(f"Request recorded: {db_request.id}")
        return db_request
    
    @staticmethod
    def get_by_id(db: Session, request_id: int) -> Request:
        """Get request by ID"""
        return db.query(Request).filter(Request.id == request_id).first()
    
    @staticmethod
    def get_by_api_key(db: Session, api_key_id: int, skip: int = 0, limit: int = 100):
        """Get requests by API key"""
        return db.query(Request).filter(
            Request.api_key_id == api_key_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_project(db: Session, project_id: int, skip: int = 0, limit: int = 100):
        """Get requests by project"""
        return db.query(Request).filter(
            Request.project_id == project_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_failed_requests(db: Session, project_id: int, skip: int = 0, limit: int = 100):
        """Get failed requests"""
        return db.query(Request).filter(
            Request.project_id == project_id,
            Request.status == "failed"
        ).offset(skip).limit(limit).all()