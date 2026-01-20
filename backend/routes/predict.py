import os
import joblib
import pandas as pd
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

from backend.middleware.auth import require_api_key

predict_bp = Blueprint("predict", __name__)

# -------------------------------------------------
# Load ML pipeline
# -------------------------------------------------
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

MODEL_PATH = os.path.join(BASE_DIR, "ml", "models", "model_pipeline.joblib")
pipeline = joblib.load(MODEL_PATH)

# -------------------------------------------------
# Candidate materials (controlled set)
# -------------------------------------------------
MATERIALS = [
    {"name": "Corrugated Box", "base_co2": 0.45},
    {"name": "Recycled Pouch", "base_co2": 0.30},
    {"name": "Biodegradable Wrap", "base_co2": 0.25}
]

SHIPPING_CO2_FACTOR = {
    "Air": 1.5,
    "Road": 1.0,
    "Sea": 0.7
}

# -------------------------------------------------
# Prediction endpoint
# -------------------------------------------------
@predict_bp.route("/predict", methods=["POST", "OPTIONS"])
@cross_origin()
@require_api_key
def predict():

    # Allow CORS preflight
    if request.method == "OPTIONS":
        return "", 200

    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    # ----------------------------
    # ML PREDICTION (single best)
    # ----------------------------
    df = pd.DataFrame([payload])

    if hasattr(pipeline, "feature_names_in_"):
        df = df.reindex(columns=pipeline.feature_names_in_, fill_value=0)

    ml_recommendation = pipeline.predict(df)[0]

    # ----------------------------
    # ANALYTICS FOR ALL MATERIALS
    # ----------------------------
    weight = float(payload.get("weight", 1))
    fragility = int(payload.get("fragility_index", 3))
    shipping = payload.get("shipping_method", "Road")

    ship_factor = SHIPPING_CO2_FACTOR.get(shipping, 1.0)

    ranked_materials = []

    for mat in MATERIALS:
        # Cost heuristic
        cost = round(12 + weight * 8 + fragility * 2, 2)

        # CO2 heuristic
        co2 = round(mat["base_co2"] * weight * ship_factor, 3)

        # Sustainability score
        score = round(
            max(0, 100 - (cost * 1.1 + co2 * 60)),
            2
        )

        ranked_materials.append({
            "material": mat["name"],
            "predicted_cost": cost,
            "co2_impact": co2,
            "sustainability_score": score,
            "ml_choice": mat["name"] == ml_recommendation
        })

    # Rank by sustainability score
    ranked_materials.sort(
        key=lambda x: x["sustainability_score"],
        reverse=True
    )

    # ----------------------------
    # FINAL RESPONSE
    # ----------------------------
    return jsonify({
        "product": {
            "shipping_method": shipping
        },
        "ml_recommendation": ml_recommendation,
        "ranked_materials": ranked_materials,
        "model_metadata": {
            "model": "RandomForestClassifier",
            "mode": "ml + analytics ranking",
            "status": "hybrid"
        }
    }), 200
