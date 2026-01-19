"""
Authentication Middleware
=========================

API key and token-based authentication.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from flask import request, jsonify, current_app
from functools import wraps
import secrets
import hashlib
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# In-memory API key store (replace with database in production)
API_KEYS = {}

def create_api_key(name, role='user'):
    """
    Create a new API key
    
    Args:
        name: API key name/identifier
        role: User role (admin, user, viewer)
        
    Returns:
        str: Generated API key
    """
    # Generate secure random key
    api_key = secrets.token_urlsafe(32)
    
    # Hash for storage
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Store with metadata
    API_KEYS[key_hash] = {
        'name': name,
        'role': role,
        'created_at': datetime.now().isoformat(),
        'last_used': None
    }
    
    logger.info(f"API key created: {name} (role: {role})")
    
    return api_key

def validate_api_key(api_key):
    """
    Validate API key
    
    Args:
        api_key: API key to validate
        
    Returns:
        dict: API key metadata if valid, None otherwise
    """
    if not api_key:
        return None
    
    # Hash the provided key
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    
    # Check if exists
    if key_hash in API_KEYS:
        # Update last used timestamp
        API_KEYS[key_hash]['last_used'] = datetime.now().isoformat()
        return API_KEYS[key_hash]
    
    return None

def require_api_key(f):
    """
    Decorator to require API key authentication
    
    Usage:
        @app.route('/api/protected')
        @require_api_key
        def protected_route():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if authentication is enabled
        if not current_app.config.get('REQUIRE_AUTH', False):
            return f(*args, **kwargs)
        
        # Get API key from header
        api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
        
        if api_key and api_key.startswith('Bearer '):
            api_key = api_key[7:]  # Remove 'Bearer ' prefix
        
        # Validate key
        key_info = validate_api_key(api_key)
        
        if not key_info:
            logger.warning(f"Invalid API key attempt from {request.remote_addr}")
            return jsonify({
                'status': 'error',
                'error': 'Unauthorized',
                'message': 'Invalid or missing API key'
            }), 401
        
        # Store key info in request context
        request.api_key_info = key_info
        
        logger.info(f"API key authenticated: {key_info['name']}")
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_auth(f):
    """
    Decorator to require any form of authentication
    (Alias for require_api_key, can be extended for JWT, OAuth, etc.)
    """
    return require_api_key(f)

def require_role(required_role):
    """
    Decorator to require specific role
    
    Args:
        required_role: Required role ('admin', 'user', 'viewer')
        
    Usage:
        @app.route('/admin/endpoint')
        @require_role('admin')
        def admin_endpoint():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check if authentication is enabled
            if not current_app.config.get('REQUIRE_AUTH', False):
                return f(*args, **kwargs)
            
            # Get key info from request
            key_info = getattr(request, 'api_key_info', None)
            
            if not key_info:
                return jsonify({
                    'status': 'error',
                    'error': 'Unauthorized',
                    'message': 'Authentication required'
                }), 401
            
            # Check role hierarchy
            role_hierarchy = {'viewer': 0, 'user': 1, 'admin': 2}
            user_level = role_hierarchy.get(key_info.get('role', 'viewer'), 0)
            required_level = role_hierarchy.get(required_role, 2)
            
            if user_level < required_level:
                logger.warning(
                    f"Insufficient permissions: {key_info['name']} "
                    f"(role: {key_info['role']}) tried to access {required_role} endpoint"
                )
                return jsonify({
                    'status': 'error',
                    'error': 'Forbidden',
                    'message': f'Insufficient permissions. Required role: {required_role}'
                }), 403
            
            return f(*args, **kwargs)
        
        # Apply require_api_key first
        return require_api_key(decorated_function)
    
    return decorator

def init_default_keys():
    """
    Initialize default API keys for development
    (DO NOT use in production)
    """
    # Create admin key
    admin_key = create_api_key('admin_default', role='admin')
    logger.info(f"Default admin API key: {admin_key}")
    
    # Create user key
    user_key = create_api_key('user_default', role='user')
    logger.info(f"Default user API key: {user_key}")
    
    return {
        'admin': admin_key,
        'user': user_key
    }
