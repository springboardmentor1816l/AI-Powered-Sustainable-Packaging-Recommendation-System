"""
Configuration Module
====================

Flask application configuration.

Author: EcoPackAI Team
Date: 2026-01-03
"""

import os
from pathlib import Path

class Config:
    """Base configuration"""
    
    # Application
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = False
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://postgres:password@localhost:5432/ecopackai_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Caching
    CACHE_TYPE = os.environ.get('CACHE_TYPE', 'SimpleCache')
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    
    # Security
    REQUIRE_AUTH = os.environ.get('REQUIRE_AUTH', 'False').lower() == 'true'
    
    # Rate Limiting
    ENABLE_RATE_LIMIT = os.environ.get('ENABLE_RATE_LIMIT', 'True').lower() == 'true'
    
    # CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'SimpleCache'
    REQUIRE_AUTH = False
    ENABLE_RATE_LIMIT = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    REQUIRE_AUTH = True
    ENABLE_RATE_LIMIT = True
    CACHE_TYPE = 'RedisCache'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'SimpleCache'
    REQUIRE_AUTH = False
    ENABLE_RATE_LIMIT = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
