from flask import Blueprint, request, jsonify
from services.ranking_service import recommend_materials

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/", methods=["POST"])
def recommend():
    return jsonify({
        "recommendations": recommend_materials(request.json)
    })
