from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database.database import get_db
from app.services.auth_service import AuthService
from app.services.usage_service import UsageService
from app.database.repositories.project_repository import ProjectRepository
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{project_id}")
async def get_project_usage(
    project_id: int,
    days: int = 30,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Get project usage statistics"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    usage = UsageService.get_project_usage(db, project_id, days)
    return usage

@router.get("/{project_id}/daily")
async def get_daily_usage(
    project_id: int,
    start_date: datetime = None,
    end_date: datetime = None,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Get daily usage breakdown"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    usage = UsageService.get_daily_usage(db, project_id, start_date, end_date)
    return usage