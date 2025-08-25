import logging
import sys
from pathlib import Path
from datetime import datetime
import colorlog


def setup_logging(log_level: str = "INFO", log_file: str = None):
    """Set up logging configuration for the application with colors."""
    
    # Create log level
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {log_level}')
    
    # Create colored formatter for console with different colors for each component
    color_formatter = colorlog.ColoredFormatter(
        '%(blue)s%(asctime)s%(reset)s - %(purple)s%(name)s%(reset)s - %(log_color)s%(levelname)s%(reset)s - %(white)s%(message)s%(reset)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green', 
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
        secondary_log_colors={},
        style='%'
    )
    
    # Create regular formatter for file (without colors)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create handlers
    handlers = []
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(color_formatter)
    handlers.append(console_handler)
    
    # File handler (if specified) without colors
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(file_formatter)
        handlers.append(file_handler)
    
    # Configure root logger
    logging.basicConfig(
        level=numeric_level,
        handlers=handlers,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Suppress some noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('neo4j').setLevel(logging.WARNING)
    logging.getLogger('qdrant_client').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(name)
