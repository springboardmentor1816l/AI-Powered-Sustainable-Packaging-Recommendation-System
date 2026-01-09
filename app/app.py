import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

# ---------------- PATH SETUP ----------------
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

# ---------------- IMPORT ROUTES ----------------
from routes.predict import predict_bp
from extensions import cache
from backend.db.base import db

app = Flask(__name__)
CORS(app)

# ---------------- CONFIG ----------------
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:Ravi%40384@localhost:5432/packaging_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CACHE_TYPE"] = "SimpleCache"

# ---------------- INIT ----------------
cache.init_app(app)
db.init_app(app)
migrate = Migrate(app, db)

# ---------------- REGISTER ROUTES ----------------
app.register_blueprint(predict_bp)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "Packaging AI API"}), 200

if __name__ == "__main__":
    print("Starting server on port 5001...")
    app.run(host="0.0.0.0", port=5001, debug=True)
