# ------------------------
# Standard Imports
# ------------------------
from flask import Flask, jsonify
from flask_caching import Cache
import logging

# ------------------------
# Logging Configuration
# ------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# ------------------------
# Create Flask App
# ------------------------
app = Flask(__name__)

# ------------------------
# Database Configuration
# ------------------------
from models import db

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/ecopackai_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ------------------------
# Cache Configuration
# ------------------------
cache = Cache(config={"CACHE_TYPE": "SimpleCache"})
cache.init_app(app)

# ------------------------
# Register API Routes
# ------------------------
from predict import register_prediction_routes
register_prediction_routes(app)

# ------------------------
# Health Check Endpoint
# ------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "UP",
        "service": "EcoPackAI API",
        "message": "Service is running successfully"
    }), 200

# ------------------------
# Run the Flask App
# ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
