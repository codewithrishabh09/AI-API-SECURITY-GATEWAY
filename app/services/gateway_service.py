from sqlalchemy.orm import Session
from app.models.api_key import APIKey
from app.schemas.gateway import GatewayRequest, ResponseSchema
from app.database.repositories.api_key_repository import APIKeyRepository
from app.core.exceptions import InvalidAPIKeyException
from app.database.repositories.request_repository import RequestRepository
from datetime import datetime
import logging
import uuid
import time

logger = logging.getLogger(__name__)

class GatewayService:
    
    @staticmethod
    def validate_api_key(db: Session, api_key: str) -> APIKey:
        """Validate API key"""
        key_obj = APIKeyRepository.get_by_key(db, api_key)
        if not key_obj:
            raise InvalidAPIKeyException("API key not found")
        
        if not key_obj.is_active:
            raise InvalidAPIKeyException("API key is inactive")
        
        if key_obj.expires_at and key_obj.expires_at < datetime.utcnow():
            raise InvalidAPIKeyException("API key expired")
        
        # Update last used timestamp
        key_obj.last_used_at = datetime.utcnow()
        db.commit()
        
        return key_obj
    
    @staticmethod
    async def process_request(
        db: Session,
        api_key_obj: APIKey,
        request_data: GatewayRequest,
        client_ip: str
    ) -> ResponseSchema:
        """Process incoming request"""
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        try:
            # Record request
            request_record = {
                "api_key_id": api_key_obj.id,
                "project_id": api_key_obj.project_id,
                "status": "approved",
                "request_body": str(request_data.data),
                "endpoint": request_data.endpoint,
                "method": request_data.method,
                "ip_address": client_ip
            }
            
            req_obj = RequestRepository.create(db, request_record)
            
            # Forward to actual AI API (mock response)
            response_time = (time.time() - start_time) * 1000
            
            return ResponseSchema(
                status="success",
                data={"message": "Request processed"},
                request_id=request_id,
                processing_time_ms=response_time
            )
        except Exception as e:
            logger.error(f"Request processing failed: {str(e)}")
            raise