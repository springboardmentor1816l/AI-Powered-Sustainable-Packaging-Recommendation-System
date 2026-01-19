"""
EcoPackAI Flask API - Enhanced Version
=======================================

Production-ready Flask API with database integration, caching,  
security, and comprehensive logging.

Author: EcoPackAI Team
Date: 2026-01-03
Version: 2.0.0
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from pathlib import Path
import logging
from datetime import datetime
import traceback

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import configurations
from config.config import config

# Import backend components
from backend.models import db, init_db
from backend.cache import init_cache, cache
from backend.logging_config import setup_logging
from backend.middleware import RequestIDMiddleware
from backend.middleware.rate_limit import setup_rate_limiting
from backend.routes.predict import predict_bp
from backend.routes.health import health_bp
from backend.routes.recommend import recommend_bp
from backend.routes.export import export_bp

# Import predictors
from src.inference.predictor import EcoPackPredictor

# Get logger
logger = logging.getLogger(__name__)

# Application metadata
APP_VERSION = "2.0.0"
APP_NAME = "EcoPackAI API"
START_TIME = datetime.now()

def create_app(config_name='development'):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
        
    Returns:
        Flask app instance
    """
    # Initialize Flask app
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Setup logging
    setup_logging(app)
    
    logger.info("=" * 60)
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Environment: {config_name}")
    logger.info("=" * 60)
    
    # Initialize database
    try:
        init_db(app)
        logger.info("✓ Database initialized")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    # Initialize caching
    try:
        init_cache(app)
        logger.info("✓ Caching initialized")
    except Exception as e:
        logger.error(f"✗ Caching initialization failed: {e}")
    
    # Setup CORS
    CORS(app, origins=app.config.get('CORS_ORIGINS', '*'))
    logger.info("✓ CORS enabled")
    
    # Setup middleware
    RequestIDMiddleware(app)
    logger.info("✓ Request ID middleware enabled")
    
    # Setup rate limiting
    if app.config.get('ENABLE_RATE_LIMIT', False):
        try:
            setup_rate_limiting(app)
            logger.info("✓ Rate limiting enabled")
        except Exception as e:
            logger.warning(f"⚠ Rate limiting disabled: {e}")
    
    # Initialize predictor (singleton)
    predictor = None
    
    def get_predictor():
        """Get or create predictor instance"""
        nonlocal predictor
        if predictor is None:
            logger.info("Initializing ML models...")
            try:
                predictor = EcoPackPredictor()
                logger.info("✓ ML models loaded successfully")
            except Exception as e:
                logger.error(f"✗ Failed to load ML models: {e}")
                logger.error(traceback.format_exc())
                raise
        return predictor
    
    # Make predictor available to blueprints
    app.predictor = get_predictor
    
    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(recommend_bp)
    app.register_blueprint(export_bp)
    logger.info("✓ Routes registered")
    
    # Root endpoint
    @app.route('/')
    def index():
        """API root endpoint with service information"""
        return jsonify({
            "service": APP_NAME,
            "version": APP_VERSION,
            "status": "running",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": (datetime.now() - START_TIME).total_seconds(),
            "config": {
                "environment": config_name,
                "database": "enabled" if db else "disabled",
                "caching": app.config.get('CACHE_TYPE', 'disabled'),
                "auth_required": app.config.get('REQUIRE_AUTH', False),
                "rate_limiting": app.config.get('ENABLE_RATE_LIMIT', False)
            },
            "endpoints": {
                "health": "/health",
                "readiness": "/health/ready",
                "predict_cost": "/api/v1/predict/cost",
                "predict_co2": "/api/v1/predict/co2",
                "predict_all": "/api/v1/predict/all",
                "predict_batch": "/api/v1/predict/batch",
                "recommend": "/api/v1/recommend",
                "recommend_modes": "/api/v1/recommend/modes",
                "model_info": "/api/v1/models/info",
                "docs": "/api/v1/docs"
            },
            "documentation": {
                "api_docs": "/api/v1/docs",
                "github": "https://github.com/yourusername/EcoPackAI"
            }
        })
    
    # Global error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({
            "error": "Not Found",
            "message": "The requested endpoint does not exist",
            "status": 404,
            "timestamp": datetime.now().isoformat()
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logger.error(f"Internal server error: {error}")
        logger.error(traceback.format_exc())
        return jsonify({
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "status": 500,
            "timestamp": datetime.now().isoformat()
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions"""
        logger.error(f"Unhandled exception: {error}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            "error": "Internal Server Error",
            "message": str(error) if app.debug else "An unexpected error occurred",
            "status": 500,
            "timestamp": datetime.now().isoformat()
        }), 500
    
    logger.info("=" * 60)
    logger.info(f"{APP_NAME} initialization complete")
    logger.info("=" * 60)
    
    return app

# Create app instance
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # Development server
    logger.info(f"Starting development server...")
    logger.info("Running in DEVELOPMENT mode")
    logger.info("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
