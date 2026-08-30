from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.exceptions import RateLimitExceededException
from app.infrastructure.redis import redis_client
import logging

logger = logging.getLogger(__name__)

class RateLimitService:
    
    @staticmethod
    def check_rate_limit(db: Session, api_key: str, client_ip: str) -> bool:
        """Check if request is within rate limits"""
        if not settings.ENABLE_RATE_LIMITING:
            return True
        
        key = f"rate_limit:{api_key}:{client_ip}"
        
        try:
            current = redis_client.get(key)
            if current is None:
                redis_client.setex(key, settings.RATE_LIMIT_PERIOD, 1)
                return True
            
            current_count = int(current)
            if current_count >= settings.RATE_LIMIT_REQUESTS:
                raise RateLimitExceededException(
                    f"Rate limit exceeded: {settings.RATE_LIMIT_REQUESTS} requests per {settings.RATE_LIMIT_PERIOD}s"
                )
            
            redis_client.incr(key)
            return True
        except Exception as e:
            logger.error(f"Rate limit check failed: {str(e)}")
            raise

    @staticmethod
    def get_rate_limit_status(api_key: str, client_ip: str) -> dict:
        """Get current rate limit status"""
        key = f"rate_limit:{api_key}:{client_ip}"
        current = redis_client.get(key)
        
        return {
            "current_requests": int(current) if current else 0,
            "limit": settings.RATE_LIMIT_REQUESTS,
            "period": settings.RATE_LIMIT_PERIOD
        }