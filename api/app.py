from flask import Flask, jsonify, request
from api.config import SQLALCHEMY_DATABASE_URI
from api.extensions import db, cache
from api.middleware.auth import require_api_key
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


def create_app():
    app = Flask(__name__)

    # =====================
    # Configuration
    # =====================
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =====================
    # Initialize Extensions
    # =====================
    db.init_app(app)
    cache.init_app(app)

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
        from api.models.material import Material

        materials = Material.query.all()

        return jsonify([
            {
                "id": m.id,
                "name": m.name,
                "biodegradability_percent": m.biodegradability_percent,
                "co2_per_kg": m.co2_per_kg,
                "created_at": m.created_at.isoformat()
            }
            for m in materials
        ])

    # =====================
    # Predict API (will cache later)
    # =====================
    @app.route("/predict", methods=["POST"])
    def predict():
        # 🔐 AUTH FIRST
        auth_error = require_api_key()
        if auth_error:
            return auth_error
    
        # ✅ Cache ONLY valid requests
        @cache.cached(timeout=300)
        def cached_prediction():
            logging.info("Prediction request processed")

    
            data = request.get_json()
    
            if not data:
                logging.error("Invalid JSON received in /predict")
                return {"error": "Invalid JSON"}, 400

    
            return {
                "predictions": [
                    {
                        "category": data.get("category"),
                        "material_type": data.get("material_type"),
                        "biodegradability_percent": data.get("biodegradability_percent"),
                        "predicted_cost": 0.42,
                        "predicted_co2": 0.51
                    }
                ]
            }

        return cached_prediction()


    return app


# =====================
# App Entry Point
# =====================
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
