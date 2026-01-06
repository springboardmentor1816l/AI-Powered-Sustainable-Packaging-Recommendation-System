from flask import Blueprint, request, jsonify
import pandas as pd
import sys
import os

# ---------------- PATH SETUP ----------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../'))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.inference.predictor import MaterialSuitabilityPredictor

predict_bp = Blueprint("predict", __name__)

# ---------------- LOAD PREDICTOR ----------------
predictor = MaterialSuitabilityPredictor(
    model_path="models/trained/material_suitability_model.pkl",
    preprocessor_path="models/preprocessing/preprocessing_pipeline.pkl"
)

# ---------------- MATERIAL DATABASE ----------------
MATERIAL_DATABASE = [
    {
        "name": "Corrugated Cardboard (Heavy Duty)",
        "strength_mpa": 80,
        "recyclability_percent": 90,
        "biodegradability_percent": 100,
        "co2_emission_kg_per_kg": 0.8,
        "ideal_weight_range": (5, 50),
        "fragility_support": 3
    },
    {
        "name": "Molded Pulp (Eco-Friendly)",
        "strength_mpa": 30,
        "recyclability_percent": 100,
        "biodegradability_percent": 100,
        "co2_emission_kg_per_kg": 0.5,
        "ideal_weight_range": (0.1, 5),
        "fragility_support": 4
    },
    {
        "name": "Styrofoam (EPS)",
        "strength_mpa": 40,
        "recyclability_percent": 10,
        "biodegradability_percent": 0,
        "co2_emission_kg_per_kg": 2.5,
        "ideal_weight_range": (0.1, 10),
        "fragility_support": 5
    }
]

# ---------------- PREDICT ENDPOINT ----------------
@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        # ---------- VALIDATION ----------
        required_fields = ["weight_capacity_kg", "fragility_index", "shipping_type"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        weight = float(data["weight_capacity_kg"])
        fragility = int(data["fragility_index"])
        shipping = data["shipping_type"]

        fragility = max(1, min(fragility, 5))

        # ---------- STEP 1: STRICT FILTER ----------
        candidates = []
        for mat in MATERIAL_DATABASE:
            min_w, max_w = mat["ideal_weight_range"]
            if min_w <= weight <= max_w and fragility <= mat["fragility_support"]:
                candidates.append(mat)

        # ---------- STEP 2: RELAX FRAGILITY ----------
        if not candidates:
            for mat in MATERIAL_DATABASE:
                min_w, max_w = mat["ideal_weight_range"]
                if min_w <= weight <= max_w:
                    candidates.append(mat)

        # ---------- STEP 3: RELAX WEIGHT (FINAL FALLBACK) ----------
        if not candidates:
            candidates = MATERIAL_DATABASE.copy()

        # ---------- RANK CANDIDATES ----------
        best_material = None
        best_score = -1
        best_explanation = None

        for mat in candidates:

            adjusted_strength = mat["strength_mpa"]

            adjusted_cost = data.get("cost_per_kg", 60) + weight * 2

            adjusted_co2 = mat["co2_emission_kg_per_kg"]
            if shipping == "International":
                adjusted_co2 *= 1.5

            input_df = pd.DataFrame([{
                "strength_mpa": adjusted_strength,
                "recyclability_percent": mat["recyclability_percent"],
                "biodegradability_percent": mat["biodegradability_percent"],
                "co2_emission_kg_per_kg": adjusted_co2,
                "fragility_index": fragility,
                "cost_per_kg": adjusted_cost
            }])

            result = predictor.predict(input_df, explain=True)
            score = result["final_score"]

            if score > best_score:
                best_score = score
                best_material = mat["name"]
                best_explanation = result["explanation"]

        # ---------- RESPONSE ----------
        return jsonify({
            "prediction": round(best_score, 2),
            "recommended_material": best_material,
            "explanation": best_explanation,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500
