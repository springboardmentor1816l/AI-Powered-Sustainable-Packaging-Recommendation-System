from flask import Blueprint, request, jsonify
import pandas as pd
import json
import logging
from pathlib import Path

from middleware.auth import require_api_key
from src.inference.predictor import EcoPackPredictor
from models.db import SessionLocal
from models.prediction_history import PredictionHistory

predict_bp = Blueprint("predict", __name__)
predictor = EcoPackPredictor()
logger = logging.getLogger(__name__)

# --------------------------------------------------
# Frontend contract (PRODUCT ONLY)
# --------------------------------------------------
PRODUCT_REQUIRED_FIELDS = {
    "product_name",
    "category",
    "product_weight",
    "fragility_index",
    "shipping_type"
}

BASE_DIR = Path(__file__).resolve().parents[1]
X_RAW_PATH = BASE_DIR / "data" / "model_input" / "X_raw.csv"

TOP_K = 5  # ✅ FINAL decision: top 5 materials


@predict_bp.before_request
def secure():
    auth_error = require_api_key()
    if auth_error:
        return auth_error


@predict_bp.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()

    if not payload or not isinstance(payload, list):
        return jsonify({"error": "Invalid input"}), 400

    product_df = pd.DataFrame(payload)

    # --------------------------------------------------
    # 1. Validate PRODUCT input only
    # --------------------------------------------------
    missing = PRODUCT_REQUIRED_FIELDS - set(product_df.columns)
    if missing:
        return jsonify({
            "error": "Missing required product features",
            "missing_features": sorted(missing)
        }), 400

    product_df = product_df[list(PRODUCT_REQUIRED_FIELDS)]

    # --------------------------------------------------
    # 2. Load X_raw (MODEL INPUT DATASET)
    # --------------------------------------------------
    if not X_RAW_PATH.exists():
        return jsonify({
            "error": "X_raw dataset not found on server"
        }), 500

    X_raw = pd.read_csv(X_RAW_PATH)

    # --------------------------------------------------
    # 3. Inject product features into X_raw
    # --------------------------------------------------
    X_raw = X_raw.copy()
    X_raw["product_name"] = product_df.loc[0, "product_name"]
    X_raw["category"] = product_df.loc[0, "category"]
    X_raw["fragility_index"] = product_df.loc[0, "fragility_index"]
    X_raw["shipping_type"] = product_df.loc[0, "shipping_type"]
    X_raw["product_weight_kg"] = product_df.loc[0, "product_weight"]

    # Category match flag
    product_category = product_df.loc[0, "category"].lower()
    product_cat_cols = [c for c in X_raw.columns if c.startswith("product_cat_")]

    def category_match(row):
        for col in product_cat_cols:
            if row[col] == 1 and product_category in col.lower():
                return 1
        return 0

    X_raw["category_match_flag"] = X_raw.apply(category_match, axis=1)

    # --------------------------------------------------
    # 4. STRICT schema alignment (NO surprises)
    # --------------------------------------------------
    EXPECTED_FEATURES = predictor.preprocessor.feature_names_in_
    missing_internal = set(EXPECTED_FEATURES) - set(X_raw.columns)

    if missing_internal:
        return jsonify({
            "error": "Internal schema mismatch",
            "missing_features": sorted(missing_internal)
        }), 500

    X_model = X_raw[list(EXPECTED_FEATURES)]

    # --------------------------------------------------
    # 5. Inference
    # --------------------------------------------------
    preds = predictor.predict_batch(X_model)
    results = pd.concat([X_raw, preds], axis=1)

    # --------------------------------------------------
    # 6. Sustainability score
    # --------------------------------------------------
    co2_min = results["predicted_co2"].min()
    co2_max = results["predicted_co2"].max()

    results["co2_norm"] = (
        (results["predicted_co2"] - co2_min)
        / (co2_max - co2_min + 1e-6)
    )

    # --------------------------------------------------
    # 6. Sustainability score (PRODUCT-AWARE, FIXED)
    # --------------------------------------------------

    # Normalize recyclability
    results["recyclability_norm"] = results["recyclability_"] / 100.0

    # Product fragility impact (higher fragility → penalize low protection)
    fragility = float(product_df.loc[0, "fragility_index"])
    results["fragility_penalty"] = (
        fragility / 5.0 * (1 - results["load_handling_score"] / 5.0)
    )

    # Weight sensitivity (heavier products penalize weak materials)
    weight = float(product_df.loc[0, "product_weight"])
    results["weight_penalty"] = (
        (weight / results["product_weight_kg"].max())
        * (1 - results["reusability_"] / 100.0)
    )

    results["sustainability_score"] = (
        0.45 * results["recyclability_norm"]
        + 0.35 * (1 - results["co2_norm"])
        - 0.10 * results["fragility_penalty"]
        - 0.10 * results["weight_penalty"]
    )

    # Safety clamp
    results["sustainability_score"] = results["sustainability_score"].clip(0, 1)

    # --------------------------------------------------
    # 7. MATERIAL-LEVEL aggregation ( FIX)
    # --------------------------------------------------
    material_scores = (
        results
        .groupby("material_type", as_index=False)
        .agg({
            "predicted_cost": "mean",
            "predicted_co2": "mean",
            "sustainability_score": "mean"
        })
        .sort_values("sustainability_score", ascending=False)
        .reset_index(drop=True)
    )

    material_scores["rank"] = material_scores.index + 1
    material_scores = material_scores.head(TOP_K)

    # --------------------------------------------------
    # 8. Persist ONE record per request ( FIX)
    # --------------------------------------------------
    db = SessionLocal()
    db.add(PredictionHistory(
        request_payload=json.dumps(product_df.iloc[0].to_dict()),
        predicted_cost=float(material_scores.iloc[0]["predicted_cost"]),
        predicted_co2=float(material_scores.iloc[0]["predicted_co2"])
    ))
    db.commit()
    db.close()

    logger.info("Prediction + recommendation processed")

    # --------------------------------------------------
    # 9. API response (frontend contract)
    # --------------------------------------------------
    response = material_scores.rename(columns={
        "material_type": "material_name"
    })

    return jsonify({
        "count": len(response),
        "recommendations": response.to_dict(orient="records")
    })
