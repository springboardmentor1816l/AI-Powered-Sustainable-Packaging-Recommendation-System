from flask import Flask, request, jsonify
from models import db
from cache.cache import cache
from middleware.auth import require_api_key
from inference.predictor import predict, FEATURES
from logging_config import logger
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ---------------- CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
cache.init_app(app)

# ---------------- HEALTH ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP", "message": "EcoPackAI Service is running"})

# ---------------- PREDICT ----------------
@app.route("/predict", methods=["POST"])
@require_api_key
@cache.cached(timeout=300, query_string=True)
def predict_endpoint():
    if not request.is_json:
        return jsonify({"error": "JSON required"}), 400

    data = request.get_json()
    if isinstance(data, dict):
        data = [data]

    X = pd.DataFrame(data)
    missing = [f for f in FEATURES if f not in X.columns]
    if missing:
        return jsonify({"error": "Missing required fields", "missing_fields": missing}), 400

    preds = predict(X)
    logger.info("Prediction request processed")

    return jsonify([
        {"input_index": i, "predicted_co2_impact": float(p)}
        for i, p in enumerate(preds)
    ])

if __name__ == "__main__":
    app.run(debug=True)
