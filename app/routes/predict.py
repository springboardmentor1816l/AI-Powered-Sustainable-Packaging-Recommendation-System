from flask import Blueprint, request, jsonify
import pandas as pd
import sys
import os

# ---------------- PATH SETUP ----------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../"))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.inference.predictor import MaterialSuitabilityPredictor

predict_bp = Blueprint("predict", __name__)

# ---------------- LOAD PREDICTOR ----------------
predictor = MaterialSuitabilityPredictor(
    model_path="models/trained/material_suitability_model.pkl",
    preprocessor_path="models/preprocessing/preprocessing_pipeline.pkl"
)

# ---------------- CATEGORY MODIFIERS ----------------
def category_modifier(category: str):
    """
    Domain logic (NOT ML):
    Adjusts strength importance and fragility sensitivity
    """
    return {
        "electronics": {"strength": 1.2, "fragility": 1.4},
        "pharmaceutical": {"strength": 1.1, "fragility": 1.5},
        "food": {"strength": 1.0, "fragility": 1.1},
        "furniture": {"strength": 1.3, "fragility": 0.8},
        "general": {"strength": 1.0, "fragility": 1.0}
    }.get(category, {"strength": 1.0, "fragility": 1.0})

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

        # -------- VALIDATION --------
        required = [
            "product_name",
            "product_category",
            "weight_capacity_kg",
            "fragility_index",
            "shipping_type"
        ]

        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        product_name = data["product_name"]
        category = data["product_category"].lower()

        weight = float(data["weight_capacity_kg"])
        fragility = max(1, min(int(data["fragility_index"]), 5))
        shipping = data["shipping_type"]

        modifiers = category_modifier(category)

        analytics = []

        # -------- EVALUATE EACH MATERIAL --------
        for mat in MATERIAL_DATABASE:

            # Weight compatibility check
            min_w, max_w = mat["ideal_weight_range"]
            if not (min_w <= weight <= max_w):
                continue

            # Strength adjustment
            adjusted_strength = mat["strength_mpa"] * modifiers["strength"]

            # Fragility penalty
            fragility_penalty = (
                abs(mat["fragility_support"] - fragility)
                * 8
                * modifiers["fragility"]
            )

            # CO₂ adjustment
            adjusted_co2 = mat["co2_emission_kg_per_kg"]
            if shipping == "International":
                adjusted_co2 *= 1.6

            # Cost estimation
            adjusted_cost = 50 + weight * 3

            # ML input
            input_df = pd.DataFrame([{
                "strength_mpa": adjusted_strength,
                "recyclability_percent": mat["recyclability_percent"],
                "biodegradability_percent": mat["biodegradability_percent"],
                "co2_emission_kg_per_kg": adjusted_co2,
                "fragility_index": fragility,
                "cost_per_kg": adjusted_cost
            }])

            raw_score = predictor.predict(input_df)[0]
            final_score = max(0, min(raw_score - fragility_penalty, 100))

            analytics.append({
                "material": mat["name"],
                "suitability_score": round(final_score, 2),
                "co2": round(adjusted_co2, 2),
                "cost": round(adjusted_cost, 2),
                "strength": round(adjusted_strength, 2),
                "recyclability": mat["recyclability_percent"],
                "biodegradability": mat["biodegradability_percent"]
            })

        # -------- SORT & PICK TOP 3 --------
        analytics.sort(
            key=lambda x: x["suitability_score"],
            reverse=True
        )

        top_n = analytics[:3]  # 👈 TOP 3 RESULTS

        # Add rank field
        ranked_results = []
        for idx, item in enumerate(top_n, start=1):
            ranked_results.append({
                "rank": idx,
                **item
            })

        return jsonify({
            "product": product_name,
            "category": category,
            "recommendations": ranked_results,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500

