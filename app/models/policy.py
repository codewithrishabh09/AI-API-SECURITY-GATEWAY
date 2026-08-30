from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Policy(Base):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    policy_type = Column(String(100), nullable=False, index=True)
    rules = Column(JSON, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    is_active = Column(Integer, default=True, index=True)
    priority = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = relationship("Project", back_populates="policies")
    
    def __repr__(self):
        return f"<Policy {self.name}>"