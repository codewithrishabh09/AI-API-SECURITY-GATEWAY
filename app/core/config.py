from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "AI API Security Gateway"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "Advanced security gateway for AI APIs"
    DEBUG: bool = False
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ai_security_gateway"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 0
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # JWT
    SECRET_KEY: str = "your-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Security
    MAX_REQUEST_SIZE: int = 10485760  # 10MB
    ENABLE_RATE_LIMITING: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60
    
    # ML Models
    ML_MODEL_PATH: str = "./ml_models"
    ENABLE_PROMPT_INJECTION_DETECTION: bool = True
    ENABLE_JAILBREAK_DETECTION: bool = True
    ENABLE_TOXICITY_DETECTION: bool = True
    ENABLE_PII_DETECTION: bool = True
    ENABLE_SECRET_DETECTION: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    # Workers
    ENABLE_AUDIT_WORKER: bool = True
    ENABLE_USAGE_WORKER: bool = True
    
    # Cost Tracking
    ENABLE_COST_TRACKING: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()