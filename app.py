from flask import Flask, jsonify
import warnings
import logging

from Scripts.api.predict import predict_blueprint
from models.db import db
from models.product import Product
from models.material import Material
from models.prediction import Prediction
from cache import cache

# ----------------------------------
# App Setup
# ----------------------------------
app = Flask(__name__)

# Config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

# Init extensions
db.init_app(app)
cache.init_app(app)

# Logging
logging.basicConfig(level=logging.INFO)

# Suppress sklearn warning noise
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# ----------------------------------
# Routes
# ----------------------------------
app.register_blueprint(predict_blueprint)

@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the EcoPackAI API",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST request required)"
        }
    }), 200

@app.route("/health")
def health():
    return {"status": "ok", "service": "EcoPackAI API"}, 200

# ----------------------------------
# Run
# ----------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
