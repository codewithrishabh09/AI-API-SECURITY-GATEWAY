import logging
import logging.handlers
from pathlib import Path
from app.core.config import settings

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    
    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger