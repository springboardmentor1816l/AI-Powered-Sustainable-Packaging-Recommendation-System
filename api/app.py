from flask import Flask, jsonify, request
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.inference.predictor import EcoPackPredictor

app = Flask(__name__)

# Load predictor once
predictor = EcoPackPredictor()

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "service": "EcoPackAI API",
        "message": "Service is running"
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        df = pd.DataFrame(data)

        results = predictor.predict(df)

        return jsonify({
            "predictions": results.to_dict(orient="records")
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
