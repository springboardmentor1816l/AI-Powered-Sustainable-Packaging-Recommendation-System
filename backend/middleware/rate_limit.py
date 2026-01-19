"""
Rate Limiting
=============

API rate limiting configuration.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging

logger = logging.getLogger(__name__)

# Initialize limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

def setup_rate_limiting(app):
    """
    Setup rate limiting for Flask app
    
    Args:
        app: Flask application instance
    """
    # Configure rate limiting
    app.config.update({
        'RATELIMIT_ENABLED': app.config.get('ENABLE_RATE_LIMIT', True),
        'RATELIMIT_STORAGE_URL': app.config.get('REDIS_URL', 'memory://'),
        'RATELIMIT_STRATEGY': 'fixed-window',
        'RATELIMIT_HEADERS_ENABLED': True,
    })
    
    # Initialize limiter
    limiter.init_app(app)
    
    logger.info("Rate limiting configured")
    
    return limiter

# Custom rate limit decorators
def rate_limit_prediction(limit="100 per hour"):
    """
    Rate limit for prediction endpoints
    
    Args:
        limit: Rate limit string (e.g., "100 per hour")
    """
    return limiter.limit(limit)

def rate_limit_batch(limit="20 per hour"):
    """
    Rate limit for batch prediction endpoints
    
    Args:
        limit: Rate limit string (e.g., "20 per hour")
    """
    return limiter.limit(limit)
