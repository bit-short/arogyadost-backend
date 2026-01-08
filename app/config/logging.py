"""
Logging configuration for Digital Brain Integration.
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Setup logging configuration for the application."""
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger("app.storage.database").setLevel(logging.INFO)
    logging.getLogger("app.storage.persistent_storage").setLevel(logging.INFO)
    logging.getLogger("app.services.user_service").setLevel(logging.INFO)
    logging.getLogger("app.services.user_context").setLevel(logging.INFO)
    
    # Reduce noise from external libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)
    
    logging.info("Logging configured successfully")