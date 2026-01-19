"""
Logging Configuration
=====================

Centralized structured logging for application and security events.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import logging
import logging.handlers
import json
from datetime import datetime
from pathlib import Path
from flask import request, g, has_request_context

class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging
    """
    
    def format(self, record):
        """Format log record as JSON"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add request context if available
        if has_request_context():
            log_data.update({
                'request_id': getattr(g, 'request_id', None),
                'method': request.method,
                'path': request.path,
                'remote_addr': request.remote_addr,
                'user_agent': request.headers.get('User-Agent')
            })
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)
        
        return json.dumps(log_data)

class RequestFilter(logging.Filter):
    """
    Filter to add request context to logs
    """
    
    def filter(self, record):
        """Add request ID to record"""
        if has_request_context():
            record.request_id = getattr(g, 'request_id', 'N/A')
        else:
            record.request_id = 'N/A'
        return True

def setup_logging(app):
    """
    Setup comprehensive logging configuration
    
    Args:
        app: Flask application instance
    """
    # Create logs directory
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    root_logger.handlers = []
    
    # === Console Handler (Development) ===
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s [%(request_id)s] %(name)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(RequestFilter())
    root_logger.addHandler(console_handler)
    
    # === Application Log File (JSON) ===
    app_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'application.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(app_handler)
    
    # === Error Log File ===
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'errors.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(error_handler)
    
    # === Security Log File ===
    security_logger = logging.getLogger('security')
    security_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'security.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(JSONFormatter())
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.INFO)
    
    # === Prediction Log File ===
    prediction_logger = logging.getLogger('prediction')
    prediction_handler = logging.handlers.RotatingFileHandler(
        log_dir / 'predictions.log',
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    prediction_handler.setLevel(logging.INFO)
    prediction_handler.setFormatter(JSONFormatter())
    prediction_logger.addHandler(prediction_handler)
    prediction_logger.setLevel(logging.INFO)
    
    # Log startup
    app.logger.info("=" * 60)
    app.logger.info("EcoPackAI API Starting")
    app.logger.info(f"Log directory: {log_dir.absolute()}")
    app.logger.info("=" * 60)
    
    return root_logger

def log_prediction(input_data, output_data, duration_ms):
    """
    Log prediction request and response
    
    Args:
        input_data: Input features
        output_data: Prediction results
        duration_ms: Prediction duration in milliseconds
    """
    prediction_logger = logging.getLogger('prediction')
    
    log_entry = {
        'input_features': list(input_data.keys()) if isinstance(input_data, dict) else 'batch',
        'predictions': output_data,
        'duration_ms': duration_ms,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if has_request_context():
        log_entry.update({
            'request_id': getattr(g, 'request_id', 'N/A'),
            'remote_addr': request.remote_addr
        })
    
    prediction_logger.info('Prediction completed', extra=log_entry)

def log_security_event(event_type, details):
    """
    Log security-related events
    
    Args:
        event_type: Type of security event
        details: Event details
    """
    security_logger = logging.getLogger('security')
    
    log_entry = {
        'event_type': event_type,
        'details': details,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if has_request_context():
        log_entry.update({
            'request_id': getattr(g, 'request_id', 'N/A'),
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        })
    
    security_logger.warning(f"Security event: {event_type}", extra=log_entry)

def log_database_operation(operation, table, details=None):
    """
    Log database operations
    
    Args:
        operation: Type of operation (CREATE, READ, UPDATE, DELETE)
        table: Table name
        details: Additional details
    """
    db_logger = logging.getLogger('database')
    
    log_entry = {
        'operation': operation,
        'table': table,
        'details': details or {},
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    if has_request_context():
        log_entry.update({
            'request_id': getattr(g, 'request_id', 'N/A')
        })
    
    db_logger.info(f"Database {operation} on {table}", extra=log_entry)
