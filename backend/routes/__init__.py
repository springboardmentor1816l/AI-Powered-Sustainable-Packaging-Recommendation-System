"""
Backend Routes Module
=====================

Flask blueprints for API endpoints.
"""

from .health import health_bp
from .predict import predict_bp

__all__ = ['health_bp', 'predict_bp']
