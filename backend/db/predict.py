from flask import request, jsonify

# Allowed values for validation
VALID_CATEGORIES = ["Food", "Electronics", "Cosmetics", "Pharmacy"]
VALID_MATERIALS = ["cardboard", "PLA", "paper", "bio_plastic"]


def register_prediction_routes(app):

    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.get_json()

        # ----------------------------
        # 1. Check if JSON is provided
        # ----------------------------
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # ----------------------------
        # 2. Required fields validation
        # ----------------------------
        required_fields = [
            "product_weight",
            "category",
            "fragility_index",
            "material_type",
            "recyclability_percent",
            "co2_emission_score"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        # ----------------------------
        # 3. Data type validation
        # ----------------------------
        if not isinstance(data["product_weight"], (int, float)):
            return jsonify({"error": "product_weight must be a number"}), 400

        if not isinstance(data["fragility_index"], int):
            return jsonify({"error": "fragility_index must be an integer"}), 400

        if data["category"] not in VALID_CATEGORIES:
            return jsonify({"error": "Invalid category value"}), 400

        if data["material_type"] not in VALID_MATERIALS:
            return jsonify({"error": "Invalid material type"}), 400

        # ----------------------------
        # 4. MOCK prediction logic
        # (real ML model comes later)
        # ----------------------------
        predicted_cost = data["product_weight"] * 50
        predicted_co2 = data["co2_emission_score"] * 1.2

        # ----------------------------
        # 5. Return response
        # ----------------------------
        return jsonify({
            "predicted_cost": predicted_cost,
            "predicted_co2": predicted_co2,
            "model_version": "v1.0",
            "status": "success"
        }), 200
