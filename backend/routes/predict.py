from flask import Blueprint, request, jsonify
from backend.services.predictor import predictor
from backend.cache import cache
from backend.middleware.auth import require_api_key
from backend.db import db
from backend.models.prediction import RecommendationLog
import logging

predict_bp = Blueprint('predict', __name__)
logger = logging.getLogger(__name__)

def make_cache_key(*args, **kwargs):
    """
    Create a cache key based on the request JSON body.
    """
    if request.is_json:
        data = request.get_json()
        # Create a deterministic string representation of the data
        # Sort keys to ensure consistent order
        import json
        return json.dumps(data, sort_keys=True)
    return request.url

@predict_bp.route('/predict', methods=['POST'])
@require_api_key
@cache.cached(timeout=60, make_cache_key=make_cache_key)
def predict():
    """
    Prediction endpoint.
    Expected Input JSON:
    {
        "product_weight_g": 150.0,
        "product_category": "electronics",
        "fragility_score": 0.8,
        "material_type": "cardboard",
        "material_recyclability_score": 0.9,
        "transport_distance_km": 500.0
    }
    """
    try:
        logger.info("Processing prediction request (not cached)")
        data = request.get_json()
        
        # Input Validation
        required_fields = [
            "product_weight_g", 
            "product_category", 
            "fragility_score", 
            "material_type",
            "material_recyclability_score",
            "transport_distance_km"
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400
            
        # Type validation (basic)
        if not isinstance(data.get("product_weight_g"), (int, float)):
             return jsonify({"error": "product_weight_g must be a number"}), 400
             
        # Run prediction
        result = predictor.predict(data)
        
        # Save to database for analytics
        try:
            prediction_log = RecommendationLog(
                product_id=None,  # We don't have product tracking yet
                recommended_material_id=None,  # We don't have material tracking yet
                cost_prediction=result['predicted_cost'],
                co2_prediction=result['predicted_co2_impact'],
                material_rank=None
            )
            db.session.add(prediction_log)
            db.session.commit()
            logger.info(f"Saved prediction to database: ID {prediction_log.rec_id}")
        except Exception as db_error:
            logger.warning(f"Failed to save prediction to database: {db_error}")
            db.session.rollback()
            # Continue even if DB save fails
        
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in /predict endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500
