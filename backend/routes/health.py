"""
Health Check Routes
===================

Provides health and readiness endpoints for monitoring and deployment.

Author: EcoPackAI Team
Date: 2026-01-02
"""

from flask import Blueprint, jsonify, current_app
from datetime import datetime
import sys
import platform
import psutil
import logging

logger = logging.getLogger(__name__)

# Create blueprint
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """
    Basic health check endpoint
    
    Returns service status without loading models.
    Used by load balancers and monitoring systems.
    
    Response:
        200: Service is healthy
        {
            "status": "healthy",
            "timestamp": "2026-01-02T11:40:00",
            "service": "EcoPackAI API",
            "version": "1.0.0"
        }
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "EcoPackAI API",
        "version": "1.0.0"
    }), 200

@health_bp.route('/health/ready', methods=['GET'])
def readiness_check():
    """
    Readiness check endpoint
    
    Verifies that models are loaded and service can handle requests.
    Used by Kubernetes readiness probes.
    
    Response:
        200: Service is ready
        503: Service is not ready
    """
    try:
        # Try to get predictor
        predictor = current_app.predictor()
        
        # Check if models are loaded
        models_loaded = (
            predictor.cost_model is not None and 
            predictor.co2_model is not None
        )
        
        if models_loaded:
            return jsonify({
                "status": "ready",
                "timestamp": datetime.now().isoformat(),
                "models": {
                    "cost_model": "loaded",
                    "co2_model": "loaded"
                }
            }), 200
        else:
            return jsonify({
                "status": "not_ready",
                "timestamp": datetime.now().isoformat(),
                "message": "Models not fully loaded"
            }), 503
            
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return jsonify({
            "status": "not_ready",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 503

@health_bp.route('/health/live', methods=['GET'])
def liveness_check():
    """
    Liveness check endpoint
    
    Verifies that the application process is running.
    Used by Kubernetes liveness probes.
    
    Response:
        200: Application is alive
    """
    return jsonify({
        "status": "alive",
        "timestamp": datetime.now().isoformat()
    }), 200

@health_bp.route('/health/detailed', methods=['GET'])
def detailed_health():
    """
    Detailed health information
    
    Provides comprehensive system and application status.
    
    Response:
        200: Detailed health information
    """
    try:
        # Get predictor
        predictor = current_app.predictor()
        
        # System information
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Model information
        model_info = predictor.get_model_info()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": {
                "name": "EcoPackAI API",
                "version": "1.0.0",
                "python_version": sys.version,
                "platform": platform.platform()
            },
            "system": {
                "cpu_usage_percent": cpu_percent,
                "memory": {
                    "total_mb": round(memory.total / (1024**2), 2),
                    "available_mb": round(memory.available / (1024**2), 2),
                    "used_percent": memory.percent
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "used_percent": disk.percent
                }
            },
            "models": {
                "cost_model": {
                    "loaded": model_info['cost_model']['loaded'],
                    "type": model_info['cost_model']['type']
                },
                "co2_model": {
                    "loaded": model_info['co2_model']['loaded'],
                    "type": model_info['co2_model']['type']
                }
            }
        }), 200
        
    except Exception as e:
        logger.error(f"Detailed health check failed: {e}")
        return jsonify({
            "status": "degraded",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 200  # Still return 200 but with degraded status
