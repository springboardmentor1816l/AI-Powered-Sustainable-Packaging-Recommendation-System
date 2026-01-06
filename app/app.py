import sys
import os

# --- 1. PATH SETUP ---
# Add the project root to path so we can import 'src' if needed
current_dir = os.path.dirname(os.path.abspath(__file__)) # .../app
project_root = os.path.dirname(current_dir) # .../Packaging-System
sys.path.append(project_root)

from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

# --- 2. CORRECT IMPORTS (Relative to where you are running) ---
# Since we run this file directly, we import from sibling folders directly.
# DO NOT use "from app.routes..."
from routes.predict import predict_bp 
from extensions import cache
from backend.db.base import db 

app = Flask(__name__)
CORS(app)

# --- 3. CONFIGURATION ---
# Update password if needed
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Ravi%40384@localhost:5432/packaging_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CACHE_TYPE"] = "SimpleCache"

# --- 4. INITIALIZATION ---
cache.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# --- 5. REGISTER ROUTES ---
app.register_blueprint(predict_bp)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "Packaging AI API"}), 200

if __name__ == "__main__":
    # --- FIX: CHANGED PORT TO 5001 TO AVOID SOCKET ERROR ---
    print("Starting app on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)