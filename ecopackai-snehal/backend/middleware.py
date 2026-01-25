"""
EcoPackAI - Authentication Middleware
Module: Backend - Security (Jan 2nd)
Output: API authentication and security middleware
"""

from functools import wraps
from flask import request, jsonify
import secrets
import hashlib
from datetime import datetime

# ============================================
# API KEY AUTHENTICATION
# ============================================

# Hardcoded API keys for demo (in production, use database)
VALID_API_KEYS = {
    'demo_key_12345': 'Demo User',
    'test_key_67890': 'Test User'
}

def require_api_key(f):
    """
    Decorator to require API key authentication
    
    Usage:
        @app.route('/protected')
        @require_api_key
        def protected_route():
            return "Protected data"
    
    Request Header:
        X-API-Key: your_api_key_here
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from header
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'API key is required',
                'status': 401
            }), 401
        
        # Validate API key
        if api_key not in VALID_API_KEYS:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid API key',
                'status': 401
            }), 401
        
        # Add user info to request context
        request.api_user = VALID_API_KEYS[api_key]
        
        return f(*args, **kwargs)
    
    return decorated_function


def generate_api_key():
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)


# ============================================
# REQUEST VALIDATION
# ============================================

def validate_request_size(max_size_mb=10):
    """
    Decorator to limit request size
    
    Usage:
        @app.route('/upload')
        @validate_request_size(max_size_mb=5)
        def upload():
            return "Upload successful"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            content_length = request.content_length
            max_bytes = max_size_mb * 1024 * 1024
            
            if content_length and content_length > max_bytes:
                return jsonify({
                    'error': 'Request Too Large',
                    'message': f'Request size exceeds {max_size_mb}MB limit',
                    'status': 413
                }), 413
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


def validate_content_type(allowed_types=['application/json']):
    """
    Decorator to validate Content-Type header
    
    Usage:
        @app.route('/api/data')
        @validate_content_type(['application/json'])
        def handle_data():
            return "Data received"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            content_type = request.content_type
            
            if content_type not in allowed_types:
                return jsonify({
                    'error': 'Unsupported Media Type',
                    'message': f'Content-Type must be one of: {", ".join(allowed_types)}',
                    'status': 415
                }), 415
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ============================================
# RATE LIMITING (Simple Implementation)
# ============================================

class SimpleRateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.requests = {}  # {ip: [(timestamp, count), ...]}
    
    def is_allowed(self, identifier, max_requests=100, window_seconds=3600):
        """
        Check if request is allowed
        
        Args:
            identifier: IP address or API key
            max_requests: Maximum requests allowed
            window_seconds: Time window in seconds
        
        Returns:
            bool: True if allowed, False if rate limit exceeded
        """
        now = datetime.now().timestamp()
        
        # Clean old entries
        if identifier in self.requests:
            self.requests[identifier] = [
                (ts, count) for ts, count in self.requests[identifier]
                if now - ts < window_seconds
            ]
        else:
            self.requests[identifier] = []
        
        # Count requests in current window
        total_requests = sum(count for _, count in self.requests[identifier])
        
        if total_requests >= max_requests:
            return False
        
        # Add new request
        self.requests[identifier].append((now, 1))
        return True


# Global rate limiter instance
rate_limiter = SimpleRateLimiter()


def rate_limit(max_requests=100, window_seconds=3600):
    """
    Decorator for rate limiting
    
    Usage:
        @app.route('/api/predict')
        @rate_limit(max_requests=10, window_seconds=60)
        def predict():
            return "Prediction result"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use IP address as identifier
            identifier = request.remote_addr
            
            if not rate_limiter.is_allowed(identifier, max_requests, window_seconds):
                return jsonify({
                    'error': 'Rate Limit Exceeded',
                    'message': f'Maximum {max_requests} requests per {window_seconds} seconds',
                    'status': 429
                }), 429
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator


# ============================================
# CORS HEADERS
# ============================================

def add_cors_headers(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-API-Key'
    return response


# ============================================
# SECURITY HEADERS
# ============================================

def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


# ============================================
# REQUEST LOGGING
# ============================================

def log_request(request_obj):
    """Log request details"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': request_obj.method,
        'path': request_obj.path,
        'ip': request_obj.remote_addr,
        'user_agent': request_obj.headers.get('User-Agent', 'Unknown')
    }
    
    # In production, send to logging service
    print(f"[REQUEST] {log_entry}")
    
    return log_entry


def log_response(response, start_time):
    """Log response details"""
    response_time = (datetime.now().timestamp() - start_time) * 1000
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'status_code': response.status_code,
        'response_time_ms': round(response_time, 2)
    }
    
    print(f"[RESPONSE] {log_entry}")
    
    return log_entry


# ============================================
# IP WHITELIST/BLACKLIST
# ============================================

BLACKLISTED_IPS = set()
WHITELISTED_IPS = set()

def check_ip_access(f):
    """
    Decorator to check IP whitelist/blacklist
    
    Usage:
        @app.route('/admin')
        @check_ip_access
        def admin_panel():
            return "Admin panel"
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        
        # Check blacklist
        if client_ip in BLACKLISTED_IPS:
            return jsonify({
                'error': 'Forbidden',
                'message': 'Access denied',
                'status': 403
            }), 403
        
        # If whitelist is configured, check it
        if WHITELISTED_IPS and client_ip not in WHITELISTED_IPS:
            return jsonify({
                'error': 'Forbidden',
                'message': 'IP not whitelisted',
                'status': 403
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


# ============================================
# INPUT SANITIZATION
# ============================================

def sanitize_string(value, max_length=1000):
    """Sanitize string input"""
    if not isinstance(value, str):
        return value
    
    # Remove potentially dangerous characters
    sanitized = value.strip()
    sanitized = sanitized[:max_length]
    
    return sanitized


def sanitize_dict(data, allowed_keys=None):
    """Sanitize dictionary input"""
    if not isinstance(data, dict):
        return data
    
    sanitized = {}
    
    for key, value in data.items():
        # Check if key is allowed
        if allowed_keys and key not in allowed_keys:
            continue
        
        # Sanitize string values
        if isinstance(value, str):
            sanitized[key] = sanitize_string(value)
        else:
            sanitized[key] = value
    
    return sanitized