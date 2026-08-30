from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserCreate, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from app.core.exceptions import AuthenticationException
from app.database.repositories.user_repository import UserRepository
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

class AuthService:
    
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """Register new user"""
        existing_user = UserRepository.get_by_email(db, user_data.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = UserRepository.get_by_username(db, user_data.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        user_data_dict = user_data.dict()
        user_data_dict['hashed_password'] = hash_password(user_data.password)
        del user_data_dict['password']
        
        user = UserRepository.create(db, UserCreate(**user_data_dict))
        return user
    
    @staticmethod
    def login_user(db: Session, email: str, password: str) -> TokenResponse:
        """Authenticate user and return tokens"""
        user = UserRepository.get_by_email(db, email)
        if not user or not verify_password(password, user.hashed_password):
            raise AuthenticationException("Invalid email or password")
        
        if not user.is_active:
            raise AuthenticationException("User account is inactive")
        
        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_refresh_token(data={"sub": str(user.id)})
        
        logger.info(f"User logged in: {user.email}")
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=1800
        )
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        """Refresh access token"""
        try:
            payload = verify_token(refresh_token)
            user_id = int(payload.get("sub"))
            
            if payload.get("type") != "refresh":
                raise AuthenticationException("Invalid token type")
            
            user = UserRepository.get_by_id(db, user_id)
            if not user:
                raise AuthenticationException("User not found")
            
            access_token = create_access_token(data={"sub": str(user.id)})
            
            return TokenResponse(
                access_token=access_token,
                refresh_token=refresh_token,
                expires_in=1800
            )
        except Exception as e:
            raise AuthenticationException(f"Token refresh failed: {str(e)}")
    
    @staticmethod
    async def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(lambda: Session())):
        """Get current authenticated user"""
        try:
            token = credentials.credentials
            payload = verify_token(token)
            user_id = int(payload.get("sub"))
            
            user = UserRepository.get_by_id(db, user_id)
            if not user:
                raise AuthenticationException("User not found")
            
            return user
        except Exception as e:
            raise AuthenticationException(str(e))