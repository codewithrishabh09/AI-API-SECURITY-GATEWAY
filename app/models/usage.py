from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Usage(Base):
    __tablename__ = "usage"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    date = Column(DateTime, default=datetime.utcnow, index=True)
    total_requests = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    total_cost = Column(Float, default=0.0)
    blocked_requests = Column(Integer, default=0)
    approved_requests = Column(Integer, default=0)
    failed_requests = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    project = relationship("Project", back_populates="usage")
    
    def __repr__(self):
        return f"<Usage {self.project_id} - {self.date}>"