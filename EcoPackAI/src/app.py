# EcoPackAI/src/app.py

from flask import Flask, request, jsonify
from inference.predictor import predict, FEATURES
from pathlib import Path
import pandas as pd
import json

# =====================
# PATHS
# =====================
BASE_DIR = Path(__file__).resolve().parents[2]
METADATA_PATH = BASE_DIR / "EcoPackAI/src/inference/metadata.json"

# =====================
# LOAD METADATA
# =====================
with open(METADATA_PATH, "r") as f:
    MODEL_METADATA = json.load(f)

# =====================
# FLASK APP
# =====================
app = Flask(__name__)

# ---------------------
# HEALTH CHECK
# ---------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "message": "EcoPackAI Service is running"
    }), 200

# ---------------------
# PREDICTION ENDPOINT
# ---------------------
@app.route("/predict", methods=["POST"])
def predict_endpoint():

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    payload = request.get_json()

    # Normalize input
    if isinstance(payload, dict):
        payload = [payload]
    elif not isinstance(payload, list):
        return jsonify({"error": "Input must be dict or list of dicts"}), 400

    try:
        X = pd.DataFrame(payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # Validate required features
    missing = [f for f in FEATURES if f not in X.columns]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing
        }), 400

    # Predict
    try:
        preds = predict(X)
    except Exception as e:
        return jsonify({"error": f"Inference failed: {str(e)}"}), 500

    # Response
    response = [
        {
            "input_index": i,
            "predicted_co2_impact": float(value),
            "model_metadata": MODEL_METADATA
        }
        for i, value in enumerate(preds)
    ]

    return jsonify(response), 200

# =====================
# RUN SERVER
# =====================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
