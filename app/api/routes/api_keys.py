from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.api_key import APIKeyCreate, APIKeyResponse, APIKeyListResponse
from app.services.auth_service import AuthService
from app.database.repositories.api_key_repository import APIKeyRepository
from app.database.repositories.project_repository import ProjectRepository
from app.core.security import generate_api_key
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/{project_id}/keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    project_id: int,
    key_data: APIKeyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Create new API key for project"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    api_key = generate_api_key()
    key_obj = APIKeyRepository.create(db, api_key, project_id, key_data.name)
    return key_obj

@router.get("/{project_id}/keys", response_model=list[APIKeyListResponse])
async def list_api_keys(
    project_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """List API keys for project"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    keys = APIKeyRepository.get_by_project(db, project_id, skip, limit)
    return keys

@router.delete("/{project_id}/keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    project_id: int,
    key_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Delete API key"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    APIKeyRepository.delete(db, key_id)

@router.post("/{project_id}/keys/{key_id}/revoke", status_code=status.HTTP_200_OK)
async def revoke_api_key(
    project_id: int,
    key_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_user)
):
    """Revoke API key"""
    project = ProjectRepository.get_by_id(db, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    if project.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    key = APIKeyRepository.revoke(db, key_id)
    return {"message": "API key revoked", "key_id": key.id}