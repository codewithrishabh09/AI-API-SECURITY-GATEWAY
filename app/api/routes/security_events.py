from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.auth_service import AuthService
from app.database.repositories.project_repository import ProjectRepository
from app.services.audit_service import AuditService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{project_id}")
async def get_security_events(
    project_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Get security events for project"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    events = AuditService.get_project_events(db, project_id, skip, limit)
    return events

@router.get("/{project_id}/alerts")
async def get_security_alerts(
    project_id: int,
    severity: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Get security alerts/high-severity events"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    alerts = AuditService.get_alerts(db, project_id, severity)
    return alerts

@router.post("/{project_id}/events/{event_id}/resolve", status_code=status.HTTP_200_OK)
async def resolve_event(
    project_id: int,
    event_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Mark security event as resolved"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    AuditService.resolve_event(db, event_id)
    return {"message": "Event resolved"}