from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String(100), nullable=False, index=True)
    severity = Column(String(50), default="medium", index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    api_key_id = Column(Integer, nullable=True, index=True)
    description = Column(Text, nullable=False)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    is_resolved = Column(Integer, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationships
    project = relationship("Project", back_populates="security_events")
    user = relationship("User", back_populates="security_events")
    
    def __repr__(self):
        return f"<SecurityEvent {self.event_type} - {self.severity}>"