import logging
from app.infrastructure.queue import message_queue
from app.database.database import SessionLocal
from app.services.audit_service import AuditService
import json

logger = logging.getLogger(__name__)

def start_audit_worker():
    """Start audit worker"""
    message_queue.connect()
    message_queue.declare_queue("security_events")
    
    def callback(ch, method, properties, body):
        try:
            db = SessionLocal()
            event_data = json.loads(body)
            
            AuditService.log_security_event(
                db,
                event_data['event_type'],
                event_data['severity'],
                event_data['project_id'],
                event_data['description'],
                event_data.get('user_id'),
                event_data.get('details')
            )
            
            ch.basic_ack(delivery_tag=method.delivery_tag)
            db.close()
        except Exception as e:
            logger.error(f"Audit worker error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    message_queue.consume("security_events", callback)
    logger.info("Audit worker started")