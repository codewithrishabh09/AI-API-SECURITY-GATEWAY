from pydantic import BaseModel
from typing import Optional, Any, Generic, TypeVar

T = TypeVar('T')

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None
    timestamp: str

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    timestamp: str
    details: Optional[dict] = None

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool = True
    data: list[T]
    total: int
    skip: int
    limit: int
    timestamp: str