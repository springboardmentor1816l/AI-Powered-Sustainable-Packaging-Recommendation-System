"""
Request ID Middleware
=====================

Add unique request ID to each request for tracking.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import uuid
from flask import request, g
import logging

logger = logging.getLogger(__name__)

class RequestIDMiddleware:
    """
    Middleware to add unique request ID to each request
    """
    
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize middleware with Flask app"""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    @staticmethod
    def before_request():
        """Generate and store request ID"""
        # Check if request ID provided in header
        request_id = request.headers.get('X-Request-ID')
        
        # Generate new ID if not provided
        if not request_id:
            request_id = str(uuid.uuid4())
        
        # Store in Flask g object
        g.request_id = request_id
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.path} "
            f"[{request_id}] from {request.remote_addr}"
        )
    
    @staticmethod
    def after_request(response):
        """Add request ID to response headers"""
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        
        return response

def get_request_id():
    """
    Get current request ID
    
    Returns:
        str: Request ID or None
    """
    return getattr(g, 'request_id', None)
