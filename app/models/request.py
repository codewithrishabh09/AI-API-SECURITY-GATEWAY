from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Request(Base):
    __tablename__ = "requests"
    
    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    status = Column(String(50), default="pending", index=True)
    request_body = Column(Text, nullable=False)
    response_body = Column(Text, nullable=True)
    endpoint = Column(String(255), nullable=False, index=True)
    method = Column(String(10), nullable=False)
    ip_address = Column(String(45), nullable=True, index=True)
    user_agent = Column(Text, nullable=True)
    response_time_ms = Column(Float, nullable=True)
    tokens_used = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    error_message = Column(Text, nullable=True)
    security_checks = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    api_key = relationship("APIKey", back_populates="requests")
    project = relationship("Project", back_populates="requests")
    
    def __repr__(self):
        return f"<Request {self.id} - {self.status}>"