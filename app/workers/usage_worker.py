import logging
from app.infrastructure.queue import message_queue
from app.database.database import SessionLocal
from app.models.usage import Usage
from datetime import datetime
import json

logger = logging.getLogger(__name__)

def start_usage_worker():
    """Start usage worker"""
    message_queue.connect()
    message_queue.declare_queue("usage_updates")
    
    def callback(ch, method, properties, body):
        try:
            db = SessionLocal()
            usage_data = json.loads(body)
            
            usage = Usage(
                project_id=usage_data['project_id'],
                total_requests=usage_data.get('total_requests', 0),
                total_tokens=usage_data.get('total_tokens', 0),
                total_cost=usage_data.get('total_cost', 0.0),
                blocked_requests=usage_data.get('blocked_requests', 0),
                approved_requests=usage_data.get('approved_requests', 0),
                failed_requests=usage_data.get('failed_requests', 0)
            )
            
            db.add(usage)
            db.commit()
            ch.basic_ack(delivery_tag=method.delivery_tag)
            db.close()
        except Exception as e:
            logger.error(f"Usage worker error: {str(e)}")
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
    
    message_queue.consume("usage_updates", callback)
    logger.info("Usage worker started")