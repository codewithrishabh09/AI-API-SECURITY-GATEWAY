from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
    status = Column(String(50), default="active", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    api_keys = relationship("APIKey", back_populates="project", cascade="all, delete-orphan")
    policies = relationship("Policy", back_populates="project", cascade="all, delete-orphan")
    requests = relationship("Request", back_populates="project", cascade="all, delete-orphan")
    security_events = relationship("SecurityEvent", back_populates="project", cascade="all, delete-orphan")
    usage = relationship("Usage", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.name}>"