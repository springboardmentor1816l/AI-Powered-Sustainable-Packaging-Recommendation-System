from flask import Blueprint, request, jsonify
from services.inference import predict_sustainability

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/", methods=["POST"])
def predict():
    """
    Predict sustainability score for a given product + material payload
    """
    payload = request.json

    score = predict_sustainability(payload)

    return jsonify({
        "predicted_sustainability": score
    })
