from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.policy import PolicyCreate, PolicyUpdate, PolicyResponse
from app.services.auth_service import AuthService
from app.database.repositories.policy_repository import PolicyRepository
from app.database.repositories.project_repository import ProjectRepository
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{project_id}/policies", response_model=PolicyResponse, status_code=status.HTTP_201_CREATED)
async def create_policy(
    project_id: int,
    policy_data: PolicyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Create security policy"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    policy = PolicyRepository.create(db, policy_data, project_id)
    return policy

@router.get("/{project_id}/policies", response_model=list[PolicyResponse])
async def list_policies(
    project_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """List security policies"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    policies = PolicyRepository.get_by_project(db, project_id, skip, limit)
    return policies

@router.put("/{project_id}/policies/{policy_id}", response_model=PolicyResponse)
async def update_policy(
    project_id: int,
    policy_id: int,
    update_data: PolicyUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Update policy"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    policy = PolicyRepository.update(db, policy_id, update_data.dict(exclude_unset=True))
    return policy

@router.delete("/{project_id}/policies/{policy_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_policy(
    project_id: int,
    policy_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Delete policy"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    PolicyRepository.delete(db, policy_id)