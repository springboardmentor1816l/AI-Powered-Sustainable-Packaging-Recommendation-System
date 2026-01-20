from flask import Blueprint, request, jsonify
from backend.services.predictor import predictor
import logging

predict_bp = Blueprint('predict', __name__)
logger = logging.getLogger(__name__)

@predict_bp.route('/predict', methods=['POST'])
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
        
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in /predict endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500
