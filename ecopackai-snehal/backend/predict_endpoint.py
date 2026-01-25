"""
EcoPackAI - Prediction Endpoint with Input Validation
Module: API Layer - Dec 30th
Output: /predict endpoint with schema validation
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import numpy as np
import pandas as pd
import joblib
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ============================================
# CONFIGURATION
# ============================================
MODELS_PATH = "C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\models"

# Create Blueprint
predict_bp = Blueprint('predict', __name__)

# ============================================
# LOAD MODELS (Global - loaded once at startup)
# ============================================
print("Loading ML models...")
try:
    preprocessor = joblib.load(f"C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\models\\processingpreprocessing_pipeline.pkl")
    rf_cost = joblib.load(f"C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\reports\\rf_cost_optimized.joblib")
    xgb_co2 = joblib.load(f"C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\ml\\reports\\xgb_co2_optimized.joblib")
    
    # Load feature configuration
    import json
    with open("C:\\Users\\sneha\\Desktop\\ecopackai\\Data\\processed\\feature_names.json", 'r') as f:
        feature_config = json.load(f)
    
    print("✓ Models loaded successfully")
    MODELS_LOADED = True
except Exception as e:
    print(f"⚠ Warning: Could not load models - {e}")
    MODELS_LOADED = False

# ============================================
# INPUT VALIDATION SCHEMA
# ============================================
REQUIRED_FIELDS = {
    # Product attributes
    'product_name': str,
    'product_category': str,
    'product_weight_kg': (int, float),
    'fragility_index': int,
    'shipping_type': str,
    
    # Material attributes (for single prediction)
    'material_type': str,
    'packaging_type': str,
    'recyclability_percent': (int, float),
    'biodegradation_days': (int, float),
    'carbon_footprint': (int, float),
    'co2_emission_per_kg': (int, float),
    'load_handling_score': int,
    'moisture_resistance': int,
    'thermal_resistance': int,
    'cost_per_unit_usd': (int, float),
    'reusability_percent': (int, float),
    'recycled_content_percent': (int, float),
    'waste_reduction_impact': (int, float)
}

VALID_CATEGORIES = [
    'Food', 'Electronics', 'Cosmetics', 'Pharmacy', 
    'Apparel', 'Industrial', 'Consumer Goods'
]

VALID_SHIPPING_TYPES = ['Air', 'Road', 'Sea']

# ============================================
# VALIDATION FUNCTIONS
# ============================================
def validate_input(data):
    """
    Validate prediction input data
    
    Args:
        data: Dictionary containing prediction input
        
    Returns:
        tuple: (is_valid, errors, validated_data)
    """
    errors = []
    validated_data = {}
    
    # Check required fields
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append(f"Missing required field: {field}")
            continue
        
        value = data[field]
        
        # Type validation
        if not isinstance(value, expected_type):
            errors.append(
                f"Invalid type for {field}: expected {expected_type}, got {type(value)}"
            )
            continue
        
        validated_data[field] = value
    
    # Value range validations
    if 'product_weight_kg' in validated_data:
        if validated_data['product_weight_kg'] <= 0:
            errors.append("product_weight_kg must be positive")
    
    if 'fragility_index' in validated_data:
        if not 1 <= validated_data['fragility_index'] <= 5:
            errors.append("fragility_index must be between 1 and 5")
    
    # Validate categorical fields
    if 'product_category' in validated_data:
        if validated_data['product_category'] not in VALID_CATEGORIES:
            errors.append(
                f"Invalid product_category. Must be one of: {', '.join(VALID_CATEGORIES)}"
            )
    
    if 'shipping_type' in validated_data:
        if validated_data['shipping_type'] not in VALID_SHIPPING_TYPES:
            errors.append(
                f"Invalid shipping_type. Must be one of: {', '.join(VALID_SHIPPING_TYPES)}"
            )
    
    # Validate percentage fields
    percentage_fields = [
        'recyclability_percent', 'reusability_percent', 
        'recycled_content_percent', 'waste_reduction_impact'
    ]
    for field in percentage_fields:
        if field in validated_data:
            if not 0 <= validated_data[field] <= 100:
                errors.append(f"{field} must be between 0 and 100")
    
    # Validate score fields (1-10)
    score_fields = ['load_handling_score', 'moisture_resistance', 'thermal_resistance']
    for field in score_fields:
        if field in validated_data:
            if not 1 <= validated_data[field] <= 10:
                errors.append(f"{field} must be between 1 and 10")
    
    is_valid = len(errors) == 0
    return is_valid, errors, validated_data


# ============================================
# PREDICTION ENDPOINT
# ============================================
@predict_bp.route('/predict', methods=['POST'])
def predict():
    """
    Prediction endpoint for cost and CO₂ estimation
    
    Request Body:
        JSON object with product and material attributes
    
    Response:
        {
            "success": true,
            "predictions": {
                "cost_usd": 12.45,
                "co2_kg": 0.876,
                "material_suitability_score": 85.3
            },
            "metadata": {
                "model_version": "1.0.0",
                "prediction_time": "2024-01-12T10:30:00",
                "confidence": "high"
            }
        }
    """
    
    # Check if models are loaded
    if not MODELS_LOADED:
        return jsonify({
            "success": False,
            "error": "Models not loaded",
            "message": "ML models are not available. Please check server configuration."
        }), 503
    
    # Get request data
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "Invalid request",
                "message": "Request body must be valid JSON"
            }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Invalid JSON",
            "message": str(e)
        }), 400
    
    # Validate input
    is_valid, errors, validated_data = validate_input(data)
    
    if not is_valid:
        return jsonify({
            "success": False,
            "error": "Validation failed",
            "errors": errors
        }), 400
    
    # Make predictions
    try:
        # Prepare features (need to match training data format)
        # This is simplified - in production, you'd need proper encoding
        features_dict = {
            'product_weight_kg': validated_data['product_weight_kg'],
            'fragility_index': validated_data['fragility_index'],
            'recyclability_percent': validated_data['recyclability_percent'],
            'biodegradation_days': validated_data['biodegradation_days'],
            'carbon_footprint': validated_data['carbon_footprint'],
            'co2_emission_per_kg': validated_data['co2_emission_per_kg'],
            'load_handling_score': validated_data['load_handling_score'],
            'moisture_resistance': validated_data['moisture_resistance'],
            'thermal_resistance': validated_data['thermal_resistance'],
            'cost_per_unit_usd': validated_data['cost_per_unit_usd'],
            'reusability_percent': validated_data['reusability_percent'],
            'recycled_content_percent': validated_data['recycled_content_percent'],
            'waste_reduction_impact': validated_data['waste_reduction_impact'],
        }
        
        # Create DataFrame
        X_raw = pd.DataFrame([features_dict])
        
        # Note: In production, you need to add encoded categorical features
        # This is a simplified version
        
        # Transform features
        X_processed = preprocessor.transform(X_raw)
        
        # Make predictions
        cost_pred = float(rf_cost.predict(X_processed)[0])
        co2_pred = float(xgb_co2.predict(X_processed)[0])
        
        # Calculate suitability score (simplified)
        suitability_score = calculate_suitability_score(validated_data)
        
        # Return predictions
        return jsonify({
            "success": True,
            "predictions": {
                "cost_usd": round(cost_pred, 2),
                "co2_kg": round(co2_pred, 4),
                "material_suitability_score": round(suitability_score, 1)
            },
            "input": {
                "product": validated_data['product_name'],
                "category": validated_data['product_category'],
                "material": validated_data['material_type'],
                "packaging": validated_data['packaging_type']
            },
            "metadata": {
                "model_version": "1.0.0",
                "prediction_time": datetime.now().isoformat(),
                "confidence": "high"
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "Prediction failed",
            "message": str(e)
        }), 500


def calculate_suitability_score(data):
    """Calculate material suitability score"""
    score = 0
    
    # Fragility match
    fragility = data['fragility_index']
    load_score = data['load_handling_score']
    
    if fragility >= 4 and load_score >= 7:
        score += 40
    elif fragility >= 2 and load_score >= 5:
        score += 30
    else:
        score += 20
    
    # Resistance scores
    moisture = data['moisture_resistance']
    thermal = data['thermal_resistance']
    
    if moisture >= 7 and thermal >= 7:
        score += 30
    elif moisture >= 5 and thermal >= 5:
        score += 20
    else:
        score += 10
    
    # Sustainability
    recyclability = data['recyclability_percent']
    if recyclability >= 80:
        score += 30
    elif recyclability >= 50:
        score += 20
    else:
        score += 10
    
    return min(score, 100)


# ============================================
# API SCHEMA ENDPOINT
# ============================================
@predict_bp.route('/predict/schema', methods=['GET'])
def get_schema():
    """Return the input schema for the prediction endpoint"""
    schema = {
        "endpoint": "/api/v1/predict",
        "method": "POST",
        "content_type": "application/json",
        "required_fields": list(REQUIRED_FIELDS.keys()),
        "field_types": {k: str(v) for k, v in REQUIRED_FIELDS.items()},
        "valid_categories": VALID_CATEGORIES,
        "valid_shipping_types": VALID_SHIPPING_TYPES,
        "example_request": {
            "product_name": "Chocolate Box",
            "product_category": "Food",
            "product_weight_kg": 0.5,
            "fragility_index": 2,
            "shipping_type": "Air",
            "material_type": "Paper/Bio-Based",
            "packaging_type": "Cardboard Boxes",
            "recyclability_percent": 98,
            "biodegradation_days": 188,
            "carbon_footprint": 0.78,
            "co2_emission_per_kg": 0.54,
            "load_handling_score": 6,
            "moisture_resistance": 5,
            "thermal_resistance": 4,
            "cost_per_unit_usd": 2.24,
            "reusability_percent": 49,
            "recycled_content_percent": 79,
            "waste_reduction_impact": 61
        }
    }
    
    return jsonify(schema), 200


# ============================================
# EXPORT BLUEPRINT
# ============================================
# This will be imported in the main app.py
# from predict_endpoint import predict_bp
# app.register_blueprint(predict_bp, url_prefix='/api/v1')