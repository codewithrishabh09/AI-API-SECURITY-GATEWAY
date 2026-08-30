import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZIPMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.infrastructure.redis import redis_client
from app.api.routes import auth, gateway, projects, api_keys, policies, usage, security_events
from app.database.database import engine, Base
from app.workers.audit_worker import start_audit_worker
from app.workers.usage_worker import start_usage_worker

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting AI API Security Gateway")
    await redis_client.connect()
    if settings.ENABLE_AUDIT_WORKER:
        start_audit_worker()
    if settings.ENABLE_USAGE_WORKER:
        start_usage_worker()
    yield
    # Shutdown
    logger.info("Shutting down AI API Security Gateway")
    await redis_client.disconnect()

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Middleware
app.add_middleware(GZIPMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(gateway.router, prefix="/api/v1/gateway", tags=["Gateway"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(api_keys.router, prefix="/api/v1/api-keys", tags=["API Keys"])
app.include_router(policies.router, prefix="/api/v1/policies", tags=["Policies"])
app.include_router(usage.router, prefix="/api/v1/usage", tags=["Usage"])
app.include_router(security_events.router, prefix="/api/v1/security-events", tags=["Security Events"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.API_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )