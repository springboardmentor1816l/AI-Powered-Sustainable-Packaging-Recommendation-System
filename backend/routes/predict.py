from flask import Blueprint, request, jsonify
from middleware.auth import require_api_key
from extensions import db, cache
from models.prediction import Prediction

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
@require_api_key
@cache.cached(timeout=300)
def predict():
    data = request.json
    weight = data.get("product_weight_kg")
    score = data.get("Material Suitability Score")

    if not weight or not score:
        return jsonify({"error": "Invalid input"}), 400

    prediction = Prediction(
        product_weight=weight,
        score=score
    )
    db.session.add(prediction)
    db.session.commit()

    return jsonify({
        "prediction": "Suitable",
        "score": score
    })
