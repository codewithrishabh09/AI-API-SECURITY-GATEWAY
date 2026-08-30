from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class APIKeyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class APIKeyCreate(APIKeyBase):
    pass

class APIKeyResponse(APIKeyBase):
    id: int
    key: str
    project_id: int
    is_active: bool
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class APIKeyDetailResponse(APIKeyResponse):
    pass

class APIKeyListResponse(BaseModel):
    id: int
    name: str
    key: str
    is_active: bool
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    created_at: datetime