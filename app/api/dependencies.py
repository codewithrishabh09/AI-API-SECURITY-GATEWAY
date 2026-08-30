from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.auth_service import AuthService
from app.database.repositories.project_repository import ProjectRepository

async def get_current_active_user(current_user = Depends(AuthService.get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

async def get_admin_user(current_user = Depends(AuthService.get_current_user)):
    """Get current admin user"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def verify_project_ownership(project_id: int):
    """Verify project ownership"""
    async def verify(
        db: Session = Depends(get_db),
        current_user = Depends(AuthService.get_current_user)
    ):
        project = ProjectRepository.get_by_id(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Project not found"
            )
        if project.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized access to project"
            )
        return project
    return verify