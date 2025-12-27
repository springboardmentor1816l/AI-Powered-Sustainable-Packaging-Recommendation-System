from flask import Blueprint, request, jsonify
from services.inference import predict_cost, predict_co2

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/cost", methods=["POST"])
def cost():
    return jsonify({"cost": predict_cost(request.json)})

@predict_bp.route("/co2", methods=["POST"])
def co2():
    return jsonify({"co2": predict_co2(request.json)})
