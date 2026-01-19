from flask import Flask, jsonify, render_template
import warnings
import logging

from Scripts.api.predict import predict_blueprint
from models.db import db
from models.product import Product
from models.material import Material
from models.prediction import Prediction
from cache import cache
from flask_cors import CORS


# ----------------------------------
# App Setup
# ----------------------------------
app = Flask(__name__)
CORS(app)


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
    """
    Renders the main product prediction page.
    Ensure product.html is located in the /templates folder.
    """
    return render_template("product.html")

@app.route("/health")
def health():
    return {"status": "ok", "service": "EcoPackAI API"}, 200

# ----------------------------------
# Run
# ----------------------------------
if __name__ == "__main__":
    # Note: Running on port 5000 as per your previous setup
    app.run(debug=True, port=5000)





