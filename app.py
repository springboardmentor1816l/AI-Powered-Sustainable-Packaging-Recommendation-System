from flask import Flask, request, jsonify
import pandas as pd
import joblib
import json
import os
from datetime import datetime

# Import the Unified Predictor Module from Dec 29th task
from predictor import EcoPackPredictor

app = Flask(__name__)

# --- 1. CONFIGURATION (Key Activity: Part 1) ---
PORT = 5000
MODEL_VERSION = "1.0.0"

# --- 2. INITIALIZE PREDICTOR (Key Activity: Part 2) ---
# Load paths for artifacts created in previous modules
PIPELINE_PATH = 'models/preprocessing/preprocessing_pipeline.pkl'
COST_MODEL_PATH = 'ml/models/rf_cost.joblib'
CO2_MODEL_PATH = 'ml/models/xgb_co2.joblib'

# Initialize the predictor once for high-performance serving
predictor = EcoPackPredictor(PIPELINE_PATH, COST_MODEL_PATH, CO2_MODEL_PATH)

# =================================================================
# PART 1: HEALTH CHECK ROUTE (Deliverable: app.py / health check)
# =================================================================
@app.route('/health', methods=['GET'])
def health_check():
    """
    Confirms service availability without heavy dependencies.
    Returns 200 OK status for monitoring systems.
    """
    return jsonify({
        "status": "healthy",
        "service": "EcoPackAI-Inference-Engine",
        "version": MODEL_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }), 200

# =================================================================
# PART 2: PREDICTION ENDPOINT (Deliverable: predict.py logic)
# =================================================================
@app.route('/predict', methods=['POST'])
def predict():
    """
    Inference API route that accepts structured JSON input.
    """
    # Parse JSON body
    input_data = request.get_json()

    # --- A. INPUT VALIDATION (Key Activity: Part 2) ---
    # Required fields based on the Integrated Dataset schema
    required_fields = ['product_weight_kg', 'fragility_index', 'category']
    
    # 1. Check for missing fields
    missing = [f for f in required_fields if f not in input_data]
    if missing:
        return jsonify({
            "error": "Missing required fields",
            "required_fields": missing
        }), 400

    # 2. Correct Data Types validation
    if not isinstance(input_data['product_weight_kg'], (int, float)):
        return jsonify({"error": "product_weight_kg must be numeric"}), 400

    # --- B. INFERENCE EXECUTION ---
    try:
        # Convert JSON to DataFrame for the predictor
        raw_df = pd.DataFrame([input_data])
        
        # Call the unified predictor module
        predictions = predictor.predict(raw_df)
        
        # --- C. RESPONSE FORMAT (Output Schema: PAGE 4) ---
        return jsonify({
            "status": "success",
            "predictions": {
                "predicted_cost_index": predictions['cost_index'][0],
                "predicted_co2_impact": predictions['co2_impact'][0]
            },
            "model_metadata": {
                "version": MODEL_VERSION,
                "feature_count": len(predictor.expected_features)
            }
        }), 200

    except Exception as e:
        # Handle invalid input gracefully with clear errors
        return jsonify({
            "status": "error",
            "message": f"Inference failed: {str(e)}"
        }), 500

if __name__ == '__main__':
    print(f"🚀 EcoPackAI API starting on port {PORT}...")
    app.run(debug=True, port=PORT)