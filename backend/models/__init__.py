"""
Database Models
===============

SQLAlchemy ORM models for EcoPackAI database.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from .database import db, init_db
from .material import Material
from .product import Product
from .recommendation_log import RecommendationLog
from .user import User

__all__ = [
    'db',
    'init_db',
    'Material',
    'Product',
    'RecommendationLog',
    'User'
]
