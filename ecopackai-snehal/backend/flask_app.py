"""
EcoPackAI - Flask Application Skeleton & Health Check
Module: Model Serving & API Layer - Dec 30th
Output: Flask API with health check endpoint
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================
# FLASK APPLICATION INITIALIZATION
# ============================================
app = Flask(__name__)

# Enable CORS for frontend integration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Application configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Application metadata
APP_VERSION = "1.0.0"
APP_NAME = "EcoPackAI"
API_PREFIX = "/api/v1"

# ============================================
# HEALTH CHECK ENDPOINT
# ============================================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for service monitoring
    
    Returns:
        JSON response with service status
    
    Response Format:
        {
            "status": "healthy",
            "service": "EcoPackAI",
            "version": "1.0.0",
            "timestamp": "2024-01-12T10:30:00"
        }
    """
    return jsonify({
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv('FLASK_ENV', 'production')
    }), 200


@app.route(f'{API_PREFIX}/health', methods=['GET'])
def api_health_check():
    """Extended health check with dependency verification"""
    
    health_status = {
        "status": "healthy",
        "service": APP_NAME,
        "version": APP_VERSION,
        "timestamp": datetime.now().isoformat(),
        "checks": {
            "api": "ok",
            "models": "not_loaded",  # Will be updated when models load
            "database": "not_configured"  # Will be updated when DB is added
        }
    }
    
    return jsonify(health_status), 200


# ============================================
# ROOT ENDPOINT
# ============================================
@app.route('/', methods=['GET'])
def root():
    """API root endpoint with available routes"""
    return jsonify({
        "service": APP_NAME,
        "version": APP_VERSION,
        "description": "AI-Powered Sustainable Packaging Recommendation System",
        "endpoints": {
            "health": "/health",
            "api_health": f"{API_PREFIX}/health",
            "predict": f"{API_PREFIX}/predict",
            "recommend": f"{API_PREFIX}/recommend"
        },
        "documentation": "https://github.com/your-repo/ecopackai"
    }), 200


# ============================================
# ERROR HANDLERS
# ============================================
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
    return jsonify({
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "status": 500
    }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors"""
    return jsonify({
        "error": "Bad Request",
        "message": str(error),
        "status": 400
    }), 400


# ============================================
# REQUEST LOGGING MIDDLEWARE
# ============================================
@app.before_request
def log_request():
    """Log incoming requests"""
    print(f"[{datetime.now().isoformat()}] {request.method} {request.path}")


@app.after_request
def log_response(response):
    """Log outgoing responses"""
    print(f"[{datetime.now().isoformat()}] Response: {response.status_code}")
    return response


# ============================================
# MAIN ENTRY POINT
# ============================================
if __name__ == '__main__':
    # Get configuration from environment
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    print("=" * 60)
    print(f"{APP_NAME} - Flask API Server")
    print("=" * 60)
    print(f"\n🚀 Starting server...")
    print(f"   Service: {APP_NAME} v{APP_VERSION}")
    print(f"   Host: {host}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")
    print(f"\n✓ Health check: http://{host}:{port}/health")
    print(f"✓ API health: http://{host}:{port}{API_PREFIX}/health")
    print(f"✓ Root: http://{host}:{port}/")
    print("\n" + "=" * 60)
    
    # Run application
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )