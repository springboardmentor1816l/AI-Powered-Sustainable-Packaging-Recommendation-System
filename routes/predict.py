from flask import Blueprint, request, jsonify
import pandas as pd
from src.inference.predictor import EcoPackPredictor

predict_bp = Blueprint("predict", __name__)
predictor = EcoPackPredictor()

# ------------------------------------------------------------------
# Schema (strict)
# ------------------------------------------------------------------
REQUIRED_FIELDS = {
    "packaging_type",
    "material_type",
    "supplier_region",
    "recyclability_percent",
    "recycled_content_percent",
    "reusability_percent",
    "biodegradation_time_days",
    "endoflife_disposal_percent",
    "carbon_footprint_kg_co2unit",
    "co2_emission_per_kg_estimated",
    "waste_reduction_impact_percent",
    "sustainability_target_progress_percent",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "cost_per_unit_usd",
    "annual_usage_units",
    "total_material_weight_tons",
    "supplier_sustainability_compliance_percent"
}

# ------------------------------------------------------------------
# Endpoint
# ------------------------------------------------------------------
@predict_bp.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    if not payload:
        return jsonify({"error": "Empty request body"}), 400

    if not isinstance(payload, list):
        return jsonify({"error": "Input must be a list of records"}), 400

    # Validate records
    for i, record in enumerate(payload):
        missing = REQUIRED_FIELDS - record.keys()
        if missing:
            return jsonify({
                "error": f"Record {i} missing required fields",
                "missing_fields": list(missing)
            }), 400

    try:
        df = pd.DataFrame(payload)
        preds = predictor.predict_batch(df)

        response = pd.concat([df, preds], axis=1)

        return jsonify({
            "count": len(response),
            "predictions": response.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500
