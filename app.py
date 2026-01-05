from flask import Flask, request, jsonify
import pandas as pd
import joblib
import json
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache # Task 2 Import
from models.database import db, PredictionHistory, Product
import logging
from middleware.auth import require_api_key

# Import the Unified Predictor Module from Dec 29th task
from predictor import EcoPackPredictor

app = Flask(__name__)

# --- 1. CONFIGURATION ---
PORT = 5000
MODEL_VERSION = "1.0.0"

# --- DATABASE CONFIG (Task 1) ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecopack.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- CACHING CONFIG (Task 2) ---
# Using SimpleCache for in-memory storage as per scope
app.config['CACHE_TYPE'] = 'SimpleCache' 
app.config['CACHE_DEFAULT_TIMEOUT'] = 300 # Cache results for 5 minutes
cache = Cache(app)

# Initialize DB
db.init_app(app)

# --- LOGGING CONFIG (Task 3 Preview) ---
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
)

# --- 2. INITIALIZE PREDICTOR ---
PIPELINE_PATH = 'models/preprocessing/preprocessing_pipeline.pkl'
COST_MODEL_PATH = 'ml/models/rf_cost.joblib'
CO2_MODEL_PATH = 'ml/models/xgb_co2.joblib'
predictor = EcoPackPredictor(PIPELINE_PATH, COST_MODEL_PATH, CO2_MODEL_PATH)

# =================================================================
# PART 1: HEALTH CHECK (Fast, dependency-free)
# =================================================================
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# =================================================================
# PART 2: PREDICTION ENDPOINT WITH CACHING (Task 2)
# =================================================================
@app.route('/predict', methods=['POST'])
@require_api_key
# This decorator caches the response based on the request body JSON
@cache.cached(timeout=300, make_cache_key=lambda: f"predict_{request.get_data(as_text=True)}")
def predict():
    input_data = request.get_json()

    # --- A. VALIDATION ---
    required_fields = ['product_weight_kg', 'fragility_index', 'category']
    missing = [f for f in required_fields if f not in input_data]
    if missing:
        return jsonify({"error": "Missing fields", "required": missing}), 400

    # --- B. INFERENCE & PERSISTENCE ---
    try:
        raw_df = pd.DataFrame([input_data])
        predictions = predictor.predict(raw_df)
        
        # PERSIST TO DB (Task 1)
        new_prediction = PredictionHistory(
            product_weight_kg=input_data['product_weight_kg'],
            predicted_cost_index=predictions['cost_index'][0],
            predicted_co2_impact=predictions['co2_impact'][0]
        )
        db.session.add(new_prediction)
        db.session.commit()

        logging.info(f"Prediction generated and cached for: {input_data['category']}")

        return jsonify({
            "status": "success",
            "predictions": predictions,
            "cached": False 
        }), 200

    except Exception as e:
        logging.error(f"Inference error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.after_request
def add_cache_header(response):
    # Check if the response was served from our Flask-Caching 'cache'
    # Flask-Caching adds a 'X-Cache' header automatically in some configs, 
    # but we can manually detect it by checking if the request was handled by the route
    if response.status_code == 200 and request.endpoint == 'predict':
        # If the response is already prepared and we are here, 
        # but the route logic didn't "run" (it was cached), 
        # we can identify it by a custom header we set.
        pass 
    return response

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Ensure DB tables exist
    app.run(debug=True, port=PORT)