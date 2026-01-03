from flask import Blueprint, request, jsonify
from inference.predictor import predict

predict_bp = Blueprint("predict", __name__)

REQUIRED_FIELDS = [
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "Material Type",
    "Recyclability Category",
    "Load Handling Score"
]

@predict_bp.route("/predict", methods=["POST"])
def predict_endpoint():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    missing = [f for f in REQUIRED_FIELDS if f not in data]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "missing_fields": missing
        }), 400

    try:
        result = predict(data)
        return jsonify({
            "status": "success",
            "predictions": result
        }), 200

    except Exception as e:
        return jsonify({
            "error": "Prediction failed",
            "details": str(e)
        }), 500
