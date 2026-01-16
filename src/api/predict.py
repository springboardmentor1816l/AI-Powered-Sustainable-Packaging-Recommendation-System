from flask import Blueprint, request, jsonify
from src.inference.predictor import predict
from src.db.database import db
from src.db.models.prediction import Prediction
from src.middleware.auth import require_api_key
from src.cache.cache import cache
import logging
import json
import hashlib
import pandas as pd
import os

logger = logging.getLogger("ecopack")
predict_bp = Blueprint("predict", __name__)

REQUIRED_FIELDS = {
    "product_weight",
    "material_type",
    "recyclability_score"
}

# ✅ REAL DATASET
MATERIALS_CSV = os.path.join("outputs", "material_rankings.csv")


# 🔐 Cache key depends on INPUT (safe)
def make_cache_key():
    data = request.get_json()
    raw = json.dumps(data, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


@predict_bp.route("/predict", methods=["POST"])
@require_api_key
# 🔴 Disable cache while testing (enable later)
# @cache.cached(timeout=300, key_prefix=make_cache_key)
def predict_route():

    # -------------------------------
    # 1️⃣ VALIDATION
    # -------------------------------
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()
    missing = REQUIRED_FIELDS - data.keys()
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": list(missing)
        }), 400

    product_weight = float(data["product_weight"])
    user_material = data["material_type"].lower()
    user_recyclability = float(data["recyclability_score"]) * 100

    # -------------------------------
    # 2️⃣ LOAD DATASET
    # -------------------------------
    try:
        df = pd.read_csv(MATERIALS_CSV)
    except Exception as e:
        logger.error(e)
        return jsonify({"error": "Failed to load material dataset"}), 500

    # -------------------------------
    # 3️⃣ SMART FILTERING (KEY FIX)
    # -------------------------------

    # Prefer same material, but DON'T restrict
    df["material_match"] = (
        df["Material Type"].str.lower() == user_material
    ).astype(int)

    # Recyclability similarity
    df["recyclability_diff"] = abs(df["Recyclability (%)"] - user_recyclability)

    # Smart ranking before ML
    df = df.sort_values(
        by=[
            "material_match",
            "recyclability_diff",
            "Material Suitability Score"
        ],
        ascending=[False,True, False]
    )

    # 🔥 IMPORTANT: keep variety
    df = df.drop_duplicates(subset=["Packaging Type"])

    df = df.head(40)   # search space

    results = []

    # -------------------------------
    # 4️⃣ ML PREDICTION LOOP
    # -------------------------------
    for _, row in df.iterrows():

        full_data = {
            # USER INPUT
            "product_weight_kg": product_weight,
            "Recyclability (%)": user_recyclability,

            # DATASET FEATURES (MATCH PREPROCESSOR)
            "Material Type": row["Material Type"],
            "Packaging Type": row["Packaging Type"],
            "Recycled Content (%)": row["Recycled Content (%)"],
            "Reusability (%)": row["Reusability (%)"],
            "Waste Reduction Impact (%)": row["Waste Reduction Impact (%)"],
            "Supplier Sustainability Compliance (%)": row["Supplier Sustainability Compliance (%)"],
            "Load Handling Score": row["Load Handling Score"],
            "Moisture Resistance Score": row["Moisture Resistance Score"],
            "Thermal Resistance Score": row["Thermal Resistance Score"],
            "Biodegradation Time (days)": row["Biodegradation Time (days)"],
            "Supplier Region": row["Supplier Region"],
            "Recyclability Category": row["Recyclability Category"],

            # CONTEXT
            "category": "general",
            "shipping_type": "standard",
            "fragility_index": 0.5,
        }

        try:
            prediction = predict(full_data)
        except Exception as e:
            logger.error(f"Prediction failed for {row['Packaging Type']}: {e}")
            continue

        # -------------------------------
        # 5️⃣ SAVE TO DB (AS YOU ASKED)
        # -------------------------------
        db.session.add(
            Prediction(
                predicted_cost=prediction["predicted_cost"],
                predicted_co2=prediction["predicted_co2"]
            )
        )
        db.session.commit()

        # -------------------------------
        # 6️⃣ HYBRID FINAL SCORE (INPUT-AWARE)
        # -------------------------------
        final_score = (
            0.35 * prediction["predicted_cost"] +
            0.35 * prediction["predicted_co2"] +
            0.15 * (1 - data["recyclability_score"]) +
            0.15 * (1 / (row["Material Suitability Score"] + 1))
        )

        results.append({
        "Packaging Type": row["Packaging Type"],
        "Material Type": row["Material Type"],
        "predicted_cost": round(prediction["predicted_cost"], 2),
        "predicted_co2": round(prediction["predicted_co2"], 2),
        "final_score": round(final_score, 3)
        })


    if not results:
        return jsonify({"error": "No predictions generated"}), 500

    # -------------------------------
    # 7️⃣ TOP 7 RESULTS
    # -------------------------------
    results = sorted(results, key=lambda x: x["final_score"])[:7]

    for i, r in enumerate(results, start=1):
        r["rank"] = i

    # -------------------------------
    # 8️⃣ RESPONSE
    # -------------------------------
    return jsonify({
        "model_version": "v4-hybrid-ml-dynamic",
        "recommendations": results
    }), 200
