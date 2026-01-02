"""
Prediction Routes
=================

API endpoints for material cost and CO₂ predictions.
Includes input validation and error handling.

Author: EcoPackAI Team
Date: 2026-01-02
"""

from flask import Blueprint, jsonify, request, current_app
from datetime import datetime
import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

# Create blueprint
predict_bp = Blueprint('predict', __name__, url_prefix='/api/v1')

# Input validation schemas
REQUIRED_FEATURES = [
    'recyclability_percent',
    'recycled_content_percent',
    'reusability_percent',
    'biodegradation_time_days',
    'end_of_life_disposal_percent',
    'carbon_footprint_kg_co2_unit',
    'waste_reduction_impact_percent',
    'sustainability_target_progress_percent',
    'load_handling_score',
    'moisture_resistance_score',
    'thermal_resistance_score',
    'annual_usage_units',
    'total_material_weight_tons',
    'supplier_sustainability_compliance_percent',
    'co2_impact_index',
    'cost_efficiency_index',
    'material_suitability_score',
    'overall_sustainability_score'
]

FEATURE_RANGES = {
    'recyclability_percent': (0, 100),
    'recycled_content_percent': (0, 100),
    'reusability_percent': (0, 100),
    'biodegradation_time_days': (0, 3650),
    'end_of_life_disposal_percent': (0, 100),
    'carbon_footprint_kg_co2_unit': (0, 50),
    'waste_reduction_impact_percent': (0, 100),
    'sustainability_target_progress_percent': (0, 100),
    'load_handling_score': (1, 10),
    'moisture_resistance_score': (1, 10),
    'thermal_resistance_score': (1, 10),
    'annual_usage_units': (0, 1000000),
    'total_material_weight_tons': (0, 1000),
    'supplier_sustainability_compliance_percent': (0, 100),
    'co2_impact_index': (0, 1),
    'cost_efficiency_index': (0, 1),
    'material_suitability_score': (0, 100),
    'overall_sustainability_score': (0, 1)
}

def validate_input(data: Dict) -> tuple:
    """
    Validate input data for predictions
    
    Args:
        data: Input dictionary
        
    Returns:
        (is_valid, error_message)
    """
    # Check if data is provided
    if not data:
        return False, "No input data provided"
    
    # Check for required features
    missing_features = []
    for feature in REQUIRED_FEATURES:
        if feature not in data:
            missing_features.append(feature)
    
    if missing_features:
        return False, f"Missing required features: {', '.join(missing_features[:5])}{'...' if len(missing_features) > 5 else ''}"
    
    # Validate data types and ranges
    invalid_features = []
    for feature, value in data.items():
        if feature in REQUIRED_FEATURES:
            # Check if numeric
            try:
                numeric_value = float(value)
            except (ValueError, TypeError):
                invalid_features.append(f"{feature} (not numeric)")
                continue
            
            # Check range if defined
            if feature in FEATURE_RANGES:
                min_val, max_val = FEATURE_RANGES[feature]
                if not (min_val <= numeric_value <= max_val):
                    invalid_features.append(
                        f"{feature} ({numeric_value} not in range [{min_val}, {max_val}])"
                    )
    
    if invalid_features:
        return False, f"Invalid feature values: {', '.join(invalid_features[:3])}{'...' if len(invalid_features) > 3 else ''}"
    
    return True, None

def format_prediction_response(
    prediction_type: str,
    predictions: Dict,
    metadata: Dict = None
) -> Dict:
    """
    Format prediction response
    
    Args:
        prediction_type: Type of prediction ('cost', 'co2', 'all')
        predictions: Prediction results
        metadata: Optional metadata
        
    Returns:
        Formatted response dictionary
    """
    response = {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "prediction_type": prediction_type,
        "results": predictions
    }
    
    if metadata:
        response["metadata"] = metadata
    
    return response

@predict_bp.route('/predict/cost', methods=['POST'])
def predict_cost():
    """
    Predict packaging material cost
    
    Request Body:
        {
            "recyclability_percent": 95.0,
            "recycled_content_percent": 70.0,
            ... (all required features)
        }
    
    Response:
        200: Success
        {
            "status": "success",
            "timestamp": "2026-01-02T11:40:00",
            "prediction_type": "cost",
            "results": {
                "predicted_cost": 12.45,
                "cost_confidence": 0.85
            }
        }
        
        400: Invalid input
        500: Prediction error
    """
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": error_message
            }), 400
        
        # Get predictor
        predictor = current_app.predictor()
        
        # Make prediction
        logger.info("Predicting cost...")
        cost_pred, cost_conf = predictor.predict_cost(data, return_confidence=True)
        
        # Format response
        results = {
            "predicted_cost": float(cost_pred[0]),
        }
        
        if cost_conf is not None:
            results["cost_confidence"] = float(cost_conf[0])
        
        return jsonify(format_prediction_response("cost", results)), 200
        
    except Exception as e:
        logger.error(f"Cost prediction error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Prediction Error",
            "message": str(e)
        }), 500

@predict_bp.route('/predict/co2', methods=['POST'])
def predict_co2():
    """
    Predict packaging material CO₂ emissions
    
    Request Body:
        {
            "recyclability_percent": 95.0,
            "carbon_footprint_kg_co2_unit": 2.5,
            ... (all required features)
        }
    
    Response:
        200: Success
        {
            "status": "success",
            "timestamp": "2026-01-02T11:40:00",
            "prediction_type": "co2",
            "results": {
                "predicted_co2": 1.234
            }
        }
        
        400: Invalid input
        500: Prediction error
    """
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": error_message
            }), 400
        
        # Get predictor
        predictor = current_app.predictor()
        
        # Make prediction
        logger.info("Predicting CO₂...")
        co2_pred = predictor.predict_co2(data)
        
        # Format response
        results = {
            "predicted_co2": float(co2_pred[0])
        }
        
        return jsonify(format_prediction_response("co2", results)), 200
        
    except Exception as e:
        logger.error(f"CO₂ prediction error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Prediction Error",
            "message": str(e)
        }), 500

@predict_bp.route('/predict/all', methods=['POST'])
def predict_all():
    """
    Predict both cost and CO₂ emissions
    
    Request Body:
        {
            "recyclability_percent": 95.0,
            "recycled_content_percent": 70.0,
            ... (all required features)
        }
    
    Response:
        200: Success
        {
            "status": "success",
            "timestamp": "2026-01-02T11:40:00",
            "prediction_type": "all",
            "results": {
                "predicted_cost": 12.45,
                "cost_confidence": 0.85,
                "predicted_co2": 1.234
            },
            "metadata": {
                "cost_model": "Random Forest",
                "co2_model": "XGBoost"
            }
        }
        
        400: Invalid input
        500: Prediction error
    """
    try:
        # Get input data
        data = request.get_json()
        
        # Validate input
        is_valid, error_message = validate_input(data)
        if not is_valid:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": error_message
            }), 400
        
        # Get predictor
        predictor = current_app.predictor()
        
        # Make predictions
        logger.info("Predicting cost and CO₂...")
        result = predictor.predict_single(data, include_confidence=True)
        
        # Extract predictions
        results = {
            "predicted_cost": float(result.get('predicted_cost', 0)),
            "predicted_co2": float(result.get('predicted_co2', 0))
        }
        
        if 'cost_confidence' in result and result['cost_confidence']:
            results["cost_confidence"] = float(result['cost_confidence'])
        
        # Add metadata
        metadata = {
            "cost_model": "Random Forest",
            "co2_model": "XGBoost",
            "cost_r2": 0.997,
            "co2_r2": 0.994
        }
        
        return jsonify(format_prediction_response("all", results, metadata)), 200
        
    except Exception as e:
        logger.error(f"Combined prediction error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Prediction Error",
            "message": str(e)
        }), 500

@predict_bp.route('/predict/batch', methods=['POST'])
def predict_batch():
    """
    Batch prediction for multiple materials
    
    Request Body:
        {
            "materials": [
                {
                    "id": "material_1",
                    "recyclability_percent": 95.0,
                    ... (all required features)
                },
                {
                    "id": "material_2",
                    "recyclability_percent": 80.0,
                    ... (all required features)
                }
            ]
        }
    
    Response:
        200: Success with predictions for all materials
        400: Invalid input
        500: Prediction error
    """
    try:
        # Get input data
        data = request.get_json()
        
        if 'materials' not in data or not isinstance(data['materials'], list):
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": "Expected 'materials' array in request body"
            }), 400
        
        materials = data['materials']
        
        if len(materials) == 0:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": "Materials array is empty"
            }), 400
        
        # Validate each material
        validation_errors = []
        for idx, material in enumerate(materials):
            is_valid, error_message = validate_input(material)
            if not is_valid:
                validation_errors.append(f"Material {idx}: {error_message}")
        
        if validation_errors:
            return jsonify({
                "status": "error",
                "timestamp": datetime.now().isoformat(),
                "error": "Validation Error",
                "message": "Invalid materials found",
                "details": validation_errors[:5]  # Limit to first 5 errors
            }), 400
        
        # Get predictor
        predictor = current_app.predictor()
        
        # Make batch predictions
        logger.info(f"Batch predicting for {len(materials)} materials...")
        
        # Convert to DataFrame
        df_materials = pd.DataFrame(materials)
        
        # Predict
        predictions_df = predictor.predict_all(df_materials, return_confidence=True)
        
        # Format results
        results = []
        for idx, row in predictions_df.iterrows():
            result = {
                "predicted_cost": float(row.get('predicted_cost', 0)),
                "predicted_co2": float(row.get('predicted_co2', 0))
            }
            
            if 'cost_confidence' in row and pd.notna(row['cost_confidence']):
                result["cost_confidence"] = float(row['cost_confidence'])
            
            # Include ID if present
            if 'id' in materials[idx]:
                result["id"] = materials[idx]['id']
            
            results.append(result)
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "prediction_type": "batch",
            "count": len(results),
            "results": results
        }), 200
        
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": "Prediction Error",
            "message": str(e)
        }), 500

@predict_bp.route('/models/info', methods=['GET'])
def model_info():
    """
    Get information about loaded models
    
    Response:
        200: Model information
        {
            "status": "success",
            "models": {
                "cost_model": {...},
                "co2_model": {...}
            }
        }
    """
    try:
        predictor = current_app.predictor()
        info = predictor.get_model_info()
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "models": info
        }), 200
        
    except Exception as e:
        logger.error(f"Model info error: {e}")
        return jsonify({
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }), 500

@predict_bp.route('/docs', methods=['GET'])
def api_docs():
    """
    API documentation endpoint
    
    Returns API schema and usage examples
    """
    docs = {
        "api_version": "v1",
        "service": "EcoPackAI Prediction API",
        "endpoints": {
            "/api/v1/predict/cost": {
                "method": "POST",
                "description": "Predict material cost",
                "request_body": "Material features (18 required fields)",
                "response": "predicted_cost, cost_confidence"
            },
            "/api/v1/predict/co2": {
                "method": "POST",
                "description": "Predict CO₂ emissions",
                "request_body": "Material features (18 required fields)",
                "response": "predicted_co2"
            },
            "/api/v1/predict/all": {
                "method": "POST",
                "description": "Predict both cost and CO₂",
                "request_body": "Material features (18 required fields)",
                "response": "predicted_cost, predicted_co2, confidence"
            },
            "/api/v1/predict/batch": {
                "method": "POST",
                "description": "Batch prediction for multiple materials",
                "request_body": "Array of materials",
                "response": "Array of predictions"
            },
            "/api/v1/models/info": {
                "method": "GET",
                "description": "Get model information",
                "response": "Model metadata"
            }
        },
        "required_features": REQUIRED_FEATURES,
        "feature_ranges": FEATURE_RANGES,
        "example_request": {
            "recyclability_percent": 95.0,
            "recycled_content_percent": 70.0,
            "reusability_percent": 50.0,
            "biodegradation_time_days": 120,
            "end_of_life_disposal_percent": 95.0,
            "carbon_footprint_kg_co2_unit": 1.8,
            "waste_reduction_impact_percent": 80.0,
            "sustainability_target_progress_percent": 85.0,
            "load_handling_score": 8.0,
            "moisture_resistance_score": 7.0,
            "thermal_resistance_score": 7.0,
            "annual_usage_units": 15000,
            "total_material_weight_tons": 7.5,
            "supplier_sustainability_compliance_percent": 90.0,
            "co2_impact_index": 0.25,
            "cost_efficiency_index": 0.75,
            "material_suitability_score": 70.0,
            "overall_sustainability_score": 0.85
        }
    }
    
    return jsonify(docs), 200
