import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class HTTPClient:
    def __init__(self):
        self.client = None
    
    async def init(self):
        """Initialize HTTP client"""
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Close HTTP client"""
        if self.client:
            await self.client.aclose()
    
    async def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None):
        """Make POST request"""
        try:
            response = await self.client.post(url, data=data, json=json, headers=headers)
            return response
        except Exception as e:
            logger.error(f"HTTP POST error: {str(e)}")
            raise
    
    async def get(self, url: str, headers: dict = None):
        """Make GET request"""
        try:
            response = await self.client.get(url, headers=headers)
            return response
        except Exception as e:
            logger.error(f"HTTP GET error: {str(e)}")
            raise

http_client = HTTPClient()