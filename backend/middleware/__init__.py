"""
Middleware Package
==================

Authentication and request processing middleware.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from .auth import (
    require_api_key,
    require_auth,
    require_role,
    create_api_key,
    validate_api_key
)
from .request_id import RequestIDMiddleware
from .rate_limit import setup_rate_limiting

__all__ = [
    'require_api_key',
    'require_auth',
    'require_role',
    'create_api_key',
    'validate_api_key',
    'RequestIDMiddleware',
    'setup_rate_limiting'
]
