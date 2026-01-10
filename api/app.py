from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import joblib
import pandas as pd

# =========================
# Logging
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================
# Load ML Pipeline
# =========================
PIPELINE_PATH = "ml/models/material_pipeline_v1.joblib"
material_pipeline = joblib.load(PIPELINE_PATH)
logging.info("✅ Material ML pipeline loaded")

# =========================
# Category → Allowed Materials
# =========================
CATEGORY_MATERIAL_MAP = {
    "Food": ["Paper/Bio-Based", "Cardboard"],
    "Electronics": ["Plastic", "Steel"],
    "Clothing": ["Paper/Bio-Based", "Plastic"],
    "General": ["Paper/Bio-Based", "Plastic", "Steel", "Cardboard"]
}

# =========================
# Flask App
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# Health Check
# =========================
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

# =========================
# Predict Endpoint
# =========================
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        logging.info(f"RAW INPUT DATA: {data}")

        if not data:
            return jsonify({"error": "No input data"}), 400

        # -------------------------
        # Frontend inputs
        # -------------------------
        category = data.get("category", "General")
        weight = float(data.get("weight", 1.0))
        fragility = int(data.get("fragility", 3))
        shipping = data.get("shipping_type", "Ground")

        # -------------------------
        # Input mapping
        # -------------------------
        strength_map = {1: 4, 2: 5, 3: 6, 4: 7, 5: 8}
        shipping_map = {
            "Air": ("Fragile", 0.6),
            "Ground": ("General", 0.8),
            "Sea": ("Heavy", 0.9)
        }

        use_case, recyclability = shipping_map.get(
            shipping, ("General", 0.8)
        )

        strength = strength_map.get(fragility, 6)

        # -------------------------
        # Build ML input
        # -------------------------
        input_df = pd.DataFrame([{
            "packaging_type": "Box",
            "suitable_product_categories": category,
            "recommended_packaging_use_cases": use_case,
            "supplier_region": "Global",
            "recyclability_category": "High" if recyclability >= 0.75 else "Medium",
            "end_of_life_disposal_": "Recycle",

            "recyclability_": recyclability,
            "recycled_content_": round(0.4 + recyclability / 2, 2),
            "reusability_": round(0.3 + recyclability / 2, 2),
            "biodegradation_time_days_": 120 + fragility * 20,
            "carbon_footprint_kg_co2_unit_": round(0.6 - recyclability / 2, 3),
            "co2_emission_per_kg_estimated_": round(0.7 - recyclability / 2, 3),
            "waste_reduction_impact_": recyclability,
            "sustainability_target_progress_": recyclability,
            "strength": strength,
            "moisture_resistance_score": 4 + fragility,
            "thermal_resistance_score": 3 + fragility,
            "cost_per_unit_usd_": round(0.25 + fragility * 0.12, 2),
            "annual_usage_units_": int(8000 + weight * 2000),
            "total_material_weight_tons_": weight,
            "supplier_sustainability_compliance_": 0.85,
            "co2_impact_index": round(1 - recyclability, 3),
            "cost_efficiency_index": recyclability,
            "material_suitability_score": recyclability
        }])

        # -------------------------
        # ML prediction
        # -------------------------
        probabilities = material_pipeline.predict_proba(input_df)[0]
        classes = material_pipeline.classes_

        logging.info(f"Model probabilities: {dict(zip(classes, probabilities))}")

        # -------------------------
        # APPLY OPTION 1:
        # Constrained ranking by category
        # -------------------------
        allowed_materials = CATEGORY_MATERIAL_MAP.get(
            category, CATEGORY_MATERIAL_MAP["General"]
        )

        ranked = sorted(
            [
                (m, p) for m, p in zip(classes, probabilities)
                if m in allowed_materials
            ],
            key=lambda x: x[1],
            reverse=True
        )

        # -------------------------
        # Build frontend response
        # -------------------------
        predictions = []
        for material, score in ranked:
            score = float(score)

            predictions.append({
                "material_type": material,
                "predicted_cost": round(0.3 + (1 - score) * 0.5, 2),
                "predicted_co2": round(0.4 + (1 - score) * 0.6, 2),
                "biodegradability_percent": int(60 + score * 40)
            })

        return jsonify({"predictions": predictions})

    except Exception as e:
        logging.exception("❌ Prediction failed")
        return jsonify({"error": "Prediction failed"}), 500


# =========================
# App Entry Point
# =========================
if __name__ == "__main__":
    app.run(debug=True)
