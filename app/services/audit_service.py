from sqlalchemy.orm import Session
from app.models.security_event import SecurityEvent
from app.core.constants import SecurityEventType
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AuditService:
    
    @staticmethod
    def log_security_event(
        db: Session,
        event_type: str,
        severity: str,
        project_id: int,
        description: str,
        user_id: int = None,
        details: dict = None
    ) -> SecurityEvent:
        """Log security event"""
        event = SecurityEvent(
            event_type=event_type,
            severity=severity,
            project_id=project_id,
            user_id=user_id,
            description=description,
            details=details
        )
        db.add(event)
        db.commit()
        db.refresh(event)
        logger.info(f"Security event logged: {event_type} - {severity}")
        return event
    
    @staticmethod
    def get_project_events(db: Session, project_id: int, skip: int = 0, limit: int = 20):
        """Get security events for project"""
        return db.query(SecurityEvent).filter(
            SecurityEvent.project_id == project_id
        ).order_by(SecurityEvent.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_alerts(db: Session, project_id: int, severity: str = None):
        """Get high-severity alerts"""
        query = db.query(SecurityEvent).filter(
            SecurityEvent.project_id == project_id,
            SecurityEvent.is_resolved == False
        )
        
        if severity:
            query = query.filter(SecurityEvent.severity == severity)
        else:
            query = query.filter(SecurityEvent.severity.in_(["high", "critical"]))
        
        return query.order_by(SecurityEvent.created_at.desc()).all()
    
    @staticmethod
    def resolve_event(db: Session, event_id: int):
        """Mark event as resolved"""
        event = db.query(SecurityEvent).filter(SecurityEvent.id == event_id).first()
        if event:
            event.is_resolved = True
            event.resolved_at = datetime.utcnow()
            db.commit()
            logger.info(f"Security event resolved: {event.event_type}")