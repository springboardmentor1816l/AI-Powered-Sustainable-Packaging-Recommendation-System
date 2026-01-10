from flask import Blueprint, request, jsonify
import pandas as pd
import json
import logging
from middleware.auth import require_api_key
from src.inference.predictor import EcoPackPredictor
from models.db import SessionLocal
from models.prediction_history import PredictionHistory

predict_bp = Blueprint("predict", __name__)
predictor = EcoPackPredictor()
logger = logging.getLogger(__name__)

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

    df = pd.DataFrame(payload)
    EXPECTED_FEATURES = predictor.preprocessor.feature_names_in_

    missing = sorted(set(EXPECTED_FEATURES) - set(df.columns))
    extra = sorted(set(df.columns) - set(EXPECTED_FEATURES))

    if missing:
        return jsonify({
            "error": "Missing required features",
            "missing_features": missing
        }), 400

    if extra:
        return jsonify({
            "error": "Unexpected extra features",
            "extra_features": extra
        }), 400
        
    preds = predictor.predict_batch(df)

    response = pd.concat([df, preds], axis=1)

    db = SessionLocal()
    for _, row in response.iterrows():
        db.add(PredictionHistory(
            request_payload=json.dumps(row.to_dict()),
            predicted_cost=row["predicted_cost"],
            predicted_co2=row["predicted_co2"]
        ))
    db.commit()
    db.close()

    logger.info("Prediction request processed")

    return jsonify({
        "count": len(response),
        "predictions": response.to_dict(orient="records")
    })
