from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class RequestSchema(BaseModel):
    endpoint: str
    method: str
    headers: Dict[str, Any]
    body: Dict[str, Any]
    api_key: str

class ResponseSchema(BaseModel):
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    request_id: str
    processing_time_ms: float

class SecurityCheckResult(BaseModel):
    is_safe: bool
    violations: list = []
    risk_level: str
    details: Dict[str, Any]

class GatewayRequest(BaseModel):
    api_key: str
    endpoint: str
    method: str
    data: Optional[Dict[str, Any]] = None
    headers: Optional[Dict[str, str]] = None