from flask import Blueprint, request, jsonify
import numpy as np
import pandas as pd
import joblib

# Blueprint
predict_bp = Blueprint("predict", __name__)

# Load models ONCE
cost_model = joblib.load("ml/models/rf_cost.joblib")
co2_model = joblib.load("ml/models/xgb_co2.joblib")
preprocessor = joblib.load("models/preprocessing/co2_preprocessing_pipeline.pkl")

REQUIRED_FIELDS = {
    "product_weight_kg": (int, float),
    "fragility_index": int,
    "shipping_type": str,
    "category": str,
    "packaging_type": str,
    "recyclability_pct": (int, float),
    "load_handling_score": (int, float),
    "moisture_resistance_score": (int, float),
    "thermal_resistance_score": (int, float),
    "supplier_sustainability_compliance_pct": (int, float),
    "sustainability_target_progress_pct": (int, float)
}


def validate_input(payload):
    errors = []

    for field, dtype in REQUIRED_FIELDS.items():
        if field not in payload:
            errors.append(f"Missing required field: {field}")
        elif not isinstance(payload[field], dtype):
            errors.append(f"Invalid type for {field}")

    return errors


@predict_bp.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    if payload is None:
        return jsonify({"error": "Invalid JSON payload"}), 400

    errors = validate_input(payload)
    if errors:
        return jsonify({"errors": errors}), 400

    # Convert to DataFrame
    df = pd.DataFrame([payload])

    # Preprocess
    X = preprocessor.transform(df)

    # Predictions
    cost_pred = float(cost_model.predict(X)[0])
    co2_pred = float(co2_model.predict(X)[0])

    return jsonify({
        "predictions": {
            "predicted_cost_per_unit": round(cost_pred, 4),
            "predicted_co2_emission": round(co2_pred, 6)
        },
        "model_metadata": {
            "cost_model": "RandomForest v1",
            "co2_model": "XGBoost v1"
        }
    }), 200
