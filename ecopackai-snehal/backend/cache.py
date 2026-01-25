"""
EcoPackAI - Caching Setup
Module: Backend - Performance (Jan 2nd)
Output: In-memory caching for API responses
"""

from functools import wraps
from flask import request
import hashlib
import json
import time

# ============================================
# SIMPLE IN-MEMORY CACHE
# ============================================

class SimpleCache:
    """
    Simple in-memory cache with TTL (Time To Live)
    
    In production, use Redis for distributed caching
    """
    
    def __init__(self, default_ttl=300):
        """
        Initialize cache
        
        Args:
            default_ttl: Default time-to-live in seconds (default: 5 minutes)
        """
        self.cache = {}
        self.default_ttl = default_ttl
        self.stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0
        }
    
    def _is_expired(self, entry):
        """Check if cache entry is expired"""
        if entry['expires_at'] is None:
            return False
        return time.time() > entry['expires_at']
    
    def get(self, key):
        """
        Get value from cache
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self.cache:
            self.stats['misses'] += 1
            return None
        
        entry = self.cache[key]
        
        # Check if expired
        if self._is_expired(entry):
            del self.cache[key]
            self.stats['misses'] += 1
            return None
        
        self.stats['hits'] += 1
        return entry['value']
    
    def set(self, key, value, ttl=None):
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (optional)
        """
        if ttl is None:
            ttl = self.default_ttl
        
        expires_at = time.time() + ttl if ttl > 0 else None
        
        self.cache[key] = {
            'value': value,
            'expires_at': expires_at,
            'created_at': time.time()
        }
        
        self.stats['sets'] += 1
    
    def delete(self, key):
        """Delete key from cache"""
        if key in self.cache:
            del self.cache[key]
    
    def clear(self):
        """Clear all cache"""
        self.cache.clear()
        self.stats = {'hits': 0, 'misses': 0, 'sets': 0}
    
    def get_stats(self):
        """Get cache statistics"""
        total = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total * 100) if total > 0 else 0
        
        return {
            **self.stats,
            'total_requests': total,
            'hit_rate': round(hit_rate, 2),
            'size': len(self.cache)
        }
    
    def cleanup_expired(self):
        """Remove expired entries"""
        expired_keys = [
            key for key, entry in self.cache.items()
            if self._is_expired(entry)
        ]
        
        for key in expired_keys:
            del self.cache[key]
        
        return len(expired_keys)


# Global cache instance
cache = SimpleCache(default_ttl=300)  # 5 minutes default


# ============================================
# CACHE DECORATOR
# ============================================

def cached(ttl=300, key_prefix=''):
    """
    Decorator to cache function results
    
    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache key
    
    Usage:
        @cached(ttl=600, key_prefix='predict')
        def expensive_function(param1, param2):
            return result
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate cache key from function arguments
            cache_data = {
                'function': f.__name__,
                'args': args,
                'kwargs': kwargs
            }
            cache_key = f"{key_prefix}:{hashlib.md5(json.dumps(cache_data, sort_keys=True).encode()).hexdigest()}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                print(f"[CACHE HIT] {cache_key}")
                return cached_result
            
            # Execute function
            print(f"[CACHE MISS] {cache_key}")
            result = f(*args, **kwargs)
            
            # Store in cache
            cache.set(cache_key, result, ttl=ttl)
            
            return result
        
        return decorated_function
    return decorator


def cache_api_response(ttl=300):
    """
    Decorator to cache API responses based on request data
    
    Args:
        ttl: Time to live in seconds
    
    Usage:
        @app.route('/api/predict')
        @cache_api_response(ttl=600)
        def predict():
            return jsonify(result)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Only cache GET requests
            if request.method != 'GET':
                # For POST, hash the request body
                request_data = request.get_json() or {}
            else:
                request_data = dict(request.args)
            
            # Generate cache key
            cache_data = {
                'endpoint': request.endpoint,
                'method': request.method,
                'data': request_data
            }
            cache_key = hashlib.md5(
                json.dumps(cache_data, sort_keys=True).encode()
            ).hexdigest()
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                print(f"[CACHE HIT] API {request.endpoint}")
                return cached_response
            
            # Execute function
            print(f"[CACHE MISS] API {request.endpoint}")
            response = f(*args, **kwargs)
            
            # Cache successful responses only
            if isinstance(response, tuple):
                data, status_code = response
                if status_code == 200:
                    cache.set(cache_key, response, ttl=ttl)
            else:
                cache.set(cache_key, response, ttl=ttl)
            
            return response
        
        return decorated_function
    return decorator


# ============================================
# CACHE MANAGEMENT ROUTES
# ============================================

def register_cache_routes(app):
    """Register cache management routes"""
    
    @app.route('/api/v1/cache/stats', methods=['GET'])
    def cache_stats():
        """Get cache statistics"""
        return {
            'success': True,
            'stats': cache.get_stats()
        }, 200
    
    @app.route('/api/v1/cache/clear', methods=['POST'])
    def clear_cache():
        """Clear all cache"""
        cache.clear()
        return {
            'success': True,
            'message': 'Cache cleared'
        }, 200
    
    @app.route('/api/v1/cache/cleanup', methods=['POST'])
    def cleanup_cache():
        """Remove expired entries"""
        removed = cache.cleanup_expired()
        return {
            'success': True,
            'message': f'Removed {removed} expired entries'
        }, 200


# ============================================
# EXAMPLE USAGE
# ============================================

"""
Example 1: Cache function results
---------------------------------

@cached(ttl=600, key_prefix='expensive')
def expensive_calculation(x, y):
    time.sleep(2)  # Simulate expensive operation
    return x + y

result = expensive_calculation(5, 10)  # Takes 2 seconds
result = expensive_calculation(5, 10)  # Returns instantly from cache


Example 2: Cache API responses
-------------------------------

@app.route('/api/predict')
@cache_api_response(ttl=300)
def predict():
    # Expensive ML prediction
    result = model.predict(data)
    return jsonify(result)


Example 3: Manual caching
--------------------------

def get_recommendations(product_id):
    cache_key = f'recommendations:{product_id}'
    
    # Try cache first
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    # Compute recommendations
    recommendations = expensive_recommendation_logic(product_id)
    
    # Store in cache for 10 minutes
    cache.set(cache_key, recommendations, ttl=600)
    
    return recommendations
"""