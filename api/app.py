from flask import Flask, jsonify, request
from api.config import SQLALCHEMY_DATABASE_URI
from api.extensions import db

def create_app():
    app = Flask(__name__)

    # =====================
    # Configuration
    # =====================
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =====================
    # Initialize Database
    # =====================
    db.init_app(app)

    with app.app_context():
        from models.material import Material
        db.create_all()

    # =====================
    # Health Check
    # =====================
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}

    # =====================
    # Get All Materials
    # =====================
    @app.route("/materials", methods=["GET"])
    def get_materials():
        from models.material import Material

        materials = Material.query.all()

        return jsonify([
            {
                "material_id": m.material_id,
                "material_type": m.material_type,
                "strength_mpa": m.strength_mpa,
                "weight_capacity": m.weight_capacity,
                "recyclability_percent": m.recyclability_percent,
                "biodegradability_percent": m.biodegradability_percent,
                "cost_per_kg": m.cost_per_kg
            }
            for m in materials
        ])

    # =====================
    # Predict API
    # =====================
    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.get_json()

        required_fields = [
            "product_weight",
            "fragility_index",
            "shipping_type",
            "category",
            "material_type",
            "strength_mpa",
            "weight_capacity",
            "recyclability_percent",
            "biodegradability_percent"
        ]

        # Validation
        for field in required_fields:
            if field not in data or data[field] is None:
                return {
                    "error": f"Missing or invalid field: {field}"
                }, 400

        # Dummy Prediction Response
        return {
            "predictions": [
                {
                    "product_weight": data["product_weight"],
                    "fragility_index": data["fragility_index"],
                    "shipping_type": data["shipping_type"],
                    "category": data["category"],
                    "material_type": data["material_type"],
                    "strength_mpa": data["strength_mpa"],
                    "weight_capacity": data["weight_capacity"],
                    "recyclability_percent": data["recyclability_percent"],
                    "biodegradability_percent": data["biodegradability_percent"],
                    "predicted_cost": 0.42,
                    "predicted_co2": 0.51
                }
            ]
        }

    return app


# =====================
# App Entry Point
# =====================
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
