from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class SecurityEventBase(BaseModel):
    event_type: str
    severity: str
    description: str
    details: Optional[Dict[str, Any]] = None

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEventResponse(SecurityEventBase):
    id: int
    project_id: int
    user_id: Optional[int]
    api_key_id: Optional[int]
    ip_address: Optional[str]
    is_resolved: bool
    created_at: datetime
    resolved_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class SecurityAlertSchema(BaseModel):
    alert_id: str
    event_type: str
    severity: str
    timestamp: datetime
    description: str
    affected_resource: str