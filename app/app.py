# -------------------------------
# Fix Python path (important)
# -------------------------------
import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# -------------------------------
# Flask & Extensions
# -------------------------------
from flask import Flask
from flask_migrate import Migrate
from flask_caching import Cache

from backend.db.base import db
from routes.predict import predict_bp

# -------------------------------
# Create Flask app
# -------------------------------
app = Flask(__name__)

# -------------------------------
# Database Configuration
# -------------------------------
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://username:Ravi%40384@localhost:5432/packaging_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -------------------------------
# Cache Configuration (STEP 15)
# -------------------------------
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

from extensions import cache
cache.init_app(app)

# -------------------------------
# Initialize DB & Migrations
# -------------------------------
db.init_app(app)
migrate = Migrate(app, db)

# -------------------------------
# Health Check Route
# -------------------------------
@app.route("/health", methods=["GET"])
def health_check():
    return {
        "status": "ok",
        "service": "AI-Powered Sustainable Packaging API"
    }, 200

# -------------------------------
# Register Blueprints
# -------------------------------
app.register_blueprint(predict_bp)

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
