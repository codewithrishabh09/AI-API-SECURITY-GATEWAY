import pika
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class MessageQueue:
    def __init__(self):
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Connect to RabbitMQ"""
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost')
            )
            self.channel = self.connection.channel()
            logger.info("Connected to RabbitMQ")
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {str(e)}")
    
    def declare_queue(self, queue_name: str):
        """Declare queue"""
        self.channel.queue_declare(queue=queue_name, durable=True)
    
    def publish(self, queue_name: str, message: dict):
        """Publish message to queue"""
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logger.info(f"Message published to {queue_name}")
        except Exception as e:
            logger.error(f"Failed to publish message: {str(e)}")
    
    def consume(self, queue_name: str, callback):
        """Consume messages from queue"""
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=False
        )
        self.channel.start_consuming()
    
    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from RabbitMQ")

message_queue = MessageQueue()