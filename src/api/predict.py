from flask import Blueprint, request, jsonify
import joblib
import pandas as pd

predict_bp = Blueprint("predict", __name__)

# Paths
MODEL_PATH = "models/xgb_co2_model.pkl"
PREPROCESSOR_PATH = "models/preprocessing/preprocessor.joblib"

# Load once
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No input data provided"}), 400

        df = pd.DataFrame([data])

        X = preprocessor.transform(df)
        prediction = model.predict(X)[0]

        return jsonify({
            "co2_prediction": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
