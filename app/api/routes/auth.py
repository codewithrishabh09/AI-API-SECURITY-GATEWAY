from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database.database import get_db
from app.schemas.auth import UserCreate, UserLogin, UserResponse, TokenResponse, TokenRequest
from app.services.auth_service import AuthService
from app.core.exceptions import AuthenticationException, get_http_exception
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        user = AuthService.register_user(db, user_data)
        return user
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and get tokens"""
    try:
        tokens = AuthService.login_user(db, credentials.email, credentials.password)
        return tokens
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token_req: TokenRequest, db: Session = Depends(get_db)):
    """Refresh access token"""
    try:
        tokens = AuthService.refresh_access_token(db, token_req.refresh_token)
        return tokens
    except AuthenticationException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.detail
        )

@router.post("/logout")
async def logout(current_user = Depends(AuthService.get_current_user)):
    """Logout user"""
    return {"message": "Logged out successfully"}