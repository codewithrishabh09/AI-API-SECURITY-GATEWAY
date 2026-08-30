from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.gateway import GatewayRequest, ResponseSchema
from app.services.gateway_service import GatewayService
from app.services.security_service import SecurityService
from app.services.rate_limit_service import RateLimitService
from app.core.exceptions import SecurityViolationException, RateLimitExceededException
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/request", response_model=ResponseSchema)
async def gateway_request(
    request_data: GatewayRequest,
    db: Session = Depends(get_db),
    request: Request = None
):
    """Process AI API request through security gateway"""
    try:
        # Check rate limiting
        client_ip = request.client.host if request else "unknown"
        RateLimitService.check_rate_limit(db, request_data.api_key, client_ip)
        
        # Validate API key
        api_key_obj = GatewayService.validate_api_key(db, request_data.api_key)
        
        # Run security checks
        security_result = SecurityService.run_security_checks(
            db,
            request_data.data,
            api_key_obj.project_id
        )
        
        if not security_result.is_safe:
            raise SecurityViolationException(
                detail=f"Security violation detected: {', '.join(security_result.violations)}",
                violation_type=security_result.risk_level
            )
        
        # Process request
        response = await GatewayService.process_request(
            db,
            api_key_obj,
            request_data,
            client_ip
        )
        
        return response
        
    except RateLimitExceededException as e:
        raise HTTPException(status_code=429, detail=e.detail)
    except SecurityViolationException as e:
        raise HTTPException(status_code=400, detail=e.detail)
    except Exception as e:
        logger.error(f"Gateway request error: {str(e)}")
        raise HTTPException(status_code=500, detail="Request processing failed")

@router.get("/health")
async def gateway_health():
    """Check gateway health"""
    return {"status": "operational"}