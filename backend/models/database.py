"""
Database Configuration
======================

SQLAlchemy database configuration and session management.

Author: EcoPackAI Team
Date: 2026-01-03
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import logging

logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

# Initialize SQLAlchemy
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """
    Initialize database with Flask app
    
    Args:
        app: Flask application instance
    """
    # Database configuration
    db_config = {
        'SQLALCHEMY_DATABASE_URI': app.config.get(
            'DATABASE_URL',
            'postgresql://postgres:password@localhost:5432/ecopackai_db'
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': app.config.get('DEBUG', False),
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_size': 10,
            'pool_recycle': 3600,
            'pool_pre_ping': True,
            'max_overflow': 20
        }
    }
    
    app.config.update(db_config)
    
    # Initialize app
    db.init_app(app)
    
    logger.info("Database initialized successfully")
    
    return db

def create_tables(app):
    """
    Create all database tables
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.create_all()
        logger.info("Database tables created successfully")

def drop_tables(app):
    """
    Drop all database tables (USE WITH CAUTION)
    
    Args:
        app: Flask application instance
    """
    with app.app_context():
        db.drop_all()
        logger.warning("All database tables dropped")
