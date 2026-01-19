from flask import Blueprint, request, jsonify
from src.inference.predictor import Predictor

predict_blueprint = Blueprint("predict", __name__)
engine = Predictor()

@predict_blueprint.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json()

        weight = float(payload["product_weight"])
        fragility = float(payload["fragility_index"])

        # 1️⃣ Get ML predicted cost
        predicted_cost = float(engine.predict(payload))

        # 2️⃣ Compute CO2 impact
        co2_impact = round(weight * 0.75, 2)

        # 3️⃣ Rule-based material recommendation
        if fragility >= 0.7:
            material = "Molded Pulp"
        elif weight > 2:
            material = "Corrugated Cardboard"
        else:
            material = "Recycled Paper"

        return jsonify({
            "predicted_cost": round(predicted_cost, 2),
            "co2_impact": co2_impact,
            "recommended_material": material
        }), 200

    except Exception as e:
        print("🔥 Prediction Error:", e)
        return jsonify({"error": str(e)}), 500









