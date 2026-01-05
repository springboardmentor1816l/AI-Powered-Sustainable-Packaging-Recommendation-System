import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from flask import Blueprint, request, jsonify
import pandas as pd
import json
import hashlib

from extensions import cache
from security import require_api_key
from logging_config import logger
from src.inference.predictor import MaterialSuitabilityPredictor

predict_bp = Blueprint("predict", __name__)

predictor = MaterialSuitabilityPredictor()

REQUIRED_FIELDS = {
    "material_type": str,
    "industry_use_case": str,
    "source_type": str,
    "weight_capacity_kg": (int, float),
    "strength_mpa": (int, float),
    "recyclability_percent": (int, float),
    "biodegradability_percent": (int, float),
    "co2_emission_kg_per_kg": (int, float),
    "co2_impact_index": (int, float),
    "cost_efficiency_index": (int, float),
    "cost_per_kg": (int, float),
    "recyclability_category": str
}

def make_cache_key():
    payload = request.get_json(silent=True) or {}
    payload_str = json.dumps(payload, sort_keys=True)
    return hashlib.md5(payload_str.encode()).hexdigest()

@predict_bp.route("/predict", methods=["POST"])
@require_api_key
@cache.cached(timeout=300, key_prefix=make_cache_key)
def predict():

    if not request.is_json:
        logger.warning("Non-JSON request received")
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    logger.info(f"Prediction request received: {data}")

    missing_fields = [f for f in REQUIRED_FIELDS if f not in data]
    if missing_fields:
        logger.warning(f"Missing fields: {missing_fields}")
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing_fields
        }), 400

    for field, expected_type in REQUIRED_FIELDS.items():
        if not isinstance(data[field], expected_type):
            logger.warning(f"Invalid type for field: {field}")
            return jsonify({
                "error": "Invalid data type",
                "field": field,
                "expected": str(expected_type)
            }), 400

    try:
        input_df = pd.DataFrame([data])
        prediction = predictor.predict(input_df)

        logger.info(f"Prediction successful: {prediction[0]}")

        return jsonify({
            "prediction": float(prediction[0]),
            "model": "material_suitability_model",
            "cached": True,
            "status": "success"
        }), 200

    except Exception as e:
        logger.error(f"Prediction failed: {str(e)}")
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500
