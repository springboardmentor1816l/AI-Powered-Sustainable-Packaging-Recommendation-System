from flask import Blueprint, request, jsonify
from src.inference.predictor import Predictor
from cache import cache
from middleware.auth import require_api_key



predict_blueprint = Blueprint("predict", __name__)
engine = Predictor()
@predict_blueprint.before_request
def protect():
    require_api_key()


@predict_blueprint.route("/predict", methods=["POST"])
@cache.cached(timeout=60)
def predict():

    payload = request.json

    required = ["product_weight", "fragility_index", "category", "shipping_type"]
    for field in required:
        if field not in payload:
            return jsonify({"error": f"Missing field: {field}"}), 400

    result = engine.predict(payload)
    return jsonify(result), 200
