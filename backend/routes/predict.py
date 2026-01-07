from flask import Blueprint, request, jsonify
import joblib
import pandas as pd

from backend.middleware.auth import require_api_key
from backend.extensions import db
from backend.models.prediction import PredictionHistory

predict_bp = Blueprint("predict", __name__)

# ✅ REAL ML PIPELINE (loaded once)
pipeline = joblib.load("/app/ml/models/model_pipeline.joblib")

@predict_bp.route("/predict", methods=["POST"])
@require_api_key
def predict():
    payload = request.get_json()
    if not payload:
        return jsonify({"error": "Invalid JSON"}), 400

    df = pd.DataFrame([payload])

    prediction = float(pipeline.predict(df)[0])

    record = PredictionHistory(
        product_id=payload.get("product_id", 0),
        predicted_cost=prediction,
        predicted_co2=0.0,
        model_version="pipeline-v1"
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({
        "predictions": {
            "predicted_cost_per_unit": round(prediction, 4)
        },
        "model_metadata": {
            "model": "RandomForestPipeline",
            "status": "real-ml"
        }
    }), 200
