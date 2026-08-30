from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    """Repository for User model"""
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """Create new user"""
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.hashed_password,
            full_name=user_data.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User created: {db_user.email}")
        return db_user
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        """Get all users"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, user_id: int, update_data: dict) -> User:
        """Update user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in update_data.items():
                setattr(user, key, value)
            db.commit()
            db.refresh(user)
            logger.info(f"User updated: {user.email}")
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Delete user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            logger.info(f"User deleted: {user.email}")
            return True
        return False