from flask import Blueprint, request, jsonify
from middleware.auth import require_api_key

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
@require_api_key
def predict():
    data = request.get_json()

    # 1️⃣ Input validation
    weight = data.get("weight")
    fragility = data.get("fragility")
    material = data.get("material_type")

    if weight is None or fragility is None or material is None:
        return jsonify({"error": "Missing input fields"}), 400

    # 2️⃣ Simple recommendation logic (acts like ML)
    if fragility > 2:
        recommended = "paper"
        cost = 5 + weight * 2
        co2 = 0.3 * weight
    else:
        recommended = "plastic"
        cost = 4 + weight * 1.5
        co2 = 0.6 * weight

    # 3️⃣ ADD SCORE (THIS FIXES YOUR PROBLEM)
    score = round(1 / (cost + co2), 3)

    # 4️⃣ Final response
    return jsonify({
        "recommended_material": recommended,
        "estimated_cost": round(cost, 2),
        "estimated_co2": round(co2, 2),
        "score": score
    })
