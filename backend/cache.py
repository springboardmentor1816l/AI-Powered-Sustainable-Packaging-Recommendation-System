"""
Caching Configuration
=====================

In-memory and Redis-based caching for API responses.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from flask_caching import Cache
from functools import wraps
import hashlib
import json
import logging

logger = logging.getLogger(__name__)

# Initialize cache
cache = Cache()

def init_cache(app):
    """
    Initialize caching with Flask app
    
    Args:
        app: Flask application instance
    """
    # Cache configuration
    cache_type = app.config.get('CACHE_TYPE', 'SimpleCache')
    
    cache_config = {
        'CACHE_TYPE': cache_type,
        'CACHE_DEFAULT_TIMEOUT': 300,  # 5 minutes default
    }
    
    # Redis configuration (if enabled)
    if cache_type == 'RedisCache':
        cache_config.update({
            'CACHE_REDIS_URL': app.config.get('REDIS_URL', 'redis://localhost:6379/0'),
            'CACHE_KEY_PREFIX': 'ecopack_',
        })
    
    # Simple cache configuration (default)
    elif cache_type == 'SimpleCache':
        cache_config.update({
            'CACHE_THRESHOLD': 1000,  # Max 1000 items in memory
        })
    
    app.config.update(cache_config)
    cache.init_app(app)
    
    logger.info(f"Cache initialized: {cache_type}")
    
    return cache

def make_cache_key(*args, **kwargs):
    """
    Generate cache key from request data
    
    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        str: MD5 hash of the serialized data
    """
    # Serialize data
    data = {
        'args': args,
        'kwargs': kwargs
    }
    
    # Create hash
    serialized = json.dumps(data, sort_keys=True)
    key = hashlib.md5(serialized.encode()).hexdigest()
    
    return key

def cache_prediction(timeout=300):
    """
    Decorator to cache prediction results
    
    Args:
        timeout: Cache timeout in seconds (default: 300)
        
    Usage:
        @cache_prediction(timeout=600)
        def predict_cost(data):
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key
            cache_key = f"predict_{f.__name__}_{make_cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {f.__name__}")
                return cached_result
            
            # Execute function
            logger.info(f"Cache miss for {f.__name__}, executing...")
            result = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, timeout=timeout)
            
            return result
        
        return decorated_function
    return decorator

def invalidate_prediction_cache():
    """
    Invalidate all prediction-related cache entries
    """
    try:
        cache.clear()
        logger.info("Prediction cache invalidated")
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {e}")

def get_cache_stats():
    """
    Get cache statistics
    
    Returns:
        dict: Cache statistics
    """
    try:
        return {
            'type': cache.config.get('CACHE_TYPE', 'Unknown'),
            'timeout': cache.config.get('CACHE_DEFAULT_TIMEOUT', 0),
            'status': 'active'
        }
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        return {
            'type': 'Unknown',
            'status': 'error',
            'error': str(e)
        }
