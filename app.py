"""
EcoPackAI Flask API
===================

Production-ready Flask API for sustainable packaging recommendations.
Provides endpoints for health checks, predictions, and model information.

Author: EcoPackAI Team
Date: 2026-01-02
Version: 1.0.0
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
from pathlib import Path
import logging
from datetime import datetime
import traceback

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.inference.predictor import EcoPackPredictor
from backend.routes.predict import predict_bp
from backend.routes.health import health_bp

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS for all routes
CORS(app)

# Application metadata
APP_VERSION = "1.0.0"
APP_NAME = "EcoPackAI API"
START_TIME = datetime.now()

# Initialize predictor (singleton)
predictor = None

def get_predictor():
    """Get or create predictor instance (singleton pattern)"""
    global predictor
    if predictor is None:
        logger.info("Initializing EcoPackPredictor...")
        try:
            predictor = EcoPackPredictor()
            logger.info("✓ Predictor initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {e}")
            raise
    return predictor

# Make predictor available to blueprints
app.predictor = get_predictor

# Register blueprints
app.register_blueprint(health_bp)
app.register_blueprint(predict_bp)

# Root endpoint
@app.route('/')
def index():
    """API root endpoint"""
    return jsonify({
        "service": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "predict_cost": "/api/v1/predict/cost",
            "predict_co2": "/api/v1/predict/co2",
            "predict_all": "/api/v1/predict/all",
            "model_info": "/api/v1/models/info",
            "docs": "/api/v1/docs"
        }
    })

# Global error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not Found",
        "message": "The requested endpoint does not exist",
        "status": 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {error}")
    logger.error(traceback.format_exc())
    
    return jsonify({
        "error": "Internal Server Error",
        "message": str(error),
        "status": 500
    }), 500

if __name__ == '__main__':
    # Development server
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info("Running in DEVELOPMENT mode")
    logger.info("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
