import aioredis
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis = await aioredis.create_redis_pool(settings.REDIS_URL)
            logger.info("Connected to Redis")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
            logger.info("Disconnected from Redis")
    
    def set(self, key: str, value: any, ttl: int = None):
        """Set key-value pair"""
        if ttl:
            self.redis.setex(key, ttl, value)
        else:
            self.redis.set(key, value)
    
    def get(self, key: str):
        """Get value by key"""
        return self.redis.get(key)
    
    def incr(self, key: str):
        """Increment key value"""
        return self.redis.incr(key)
    
    def delete(self, key: str):
        """Delete key"""
        return self.redis.delete(key)

redis_client = RedisClient()