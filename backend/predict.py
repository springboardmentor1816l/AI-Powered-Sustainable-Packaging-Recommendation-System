from flask import request, jsonify
import joblib
import pandas as pd
import os
import sys
import yaml

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Allowed values for validation
VALID_CATEGORIES = ["Food", "Electronics", "Cosmetics", "Pharmacy"]
VALID_SHIPPING = ["Air", "Road", "Sea"]

# Load ML models and data
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'ml', 'models')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'directory')
CONFIG_DIR = os.path.join(os.path.dirname(__file__), '..', 'config')

try:
    preprocessing_pipeline = joblib.load(os.path.join(MODEL_DIR, 'preprocessing', 'preprocessing_pipeline.pkl'))
    rf_cost_model = joblib.load(os.path.join(MODEL_DIR, 'rf_cost.joblib'))
    xgb_co2_model = joblib.load(os.path.join(MODEL_DIR, 'xgb_co2.joblib'))
    materials_df = pd.read_csv(os.path.join(DATA_DIR, 'materials.csv'))
    
    # Load ranking configuration
    with open(os.path.join(CONFIG_DIR, 'ranking_weights.yaml'), 'r') as f:
        ranking_config = yaml.safe_load(f)
    
    USE_ML_MODELS = False  # Temporarily disabled due to data format mismatch
    USE_ADVANCED_RANKING = True
    print("⚠ ML models loaded but disabled - using simplified predictions")
    print("⚠ Reason: Training data format differs from current materials database")
except Exception as e:
    print(f"⚠ Warning: Could not load ML models: {e}")
    print("⚠ Using simplified predictions instead")
    USE_ML_MODELS = False
    USE_ADVANCED_RANKING = False


def calculate_simplified_sustainability(cost, co2, recyclability, category):
    """Backup simplified sustainability scoring"""
    category_weights = {
        "Food": {"cost": 0.4, "co2": 0.3, "recyclability": 0.3},
        "Electronics": {"cost": 0.3, "co2": 0.2, "recyclability": 0.5},
        "Cosmetics": {"cost": 0.5, "co2": 0.2, "recyclability": 0.3},
        "Pharmacy": {"cost": 0.35, "co2": 0.25, "recyclability": 0.4}
    }
    
    weights = category_weights.get(category, {"cost": 0.33, "co2": 0.33, "recyclability": 0.34})
    
    # Normalize metrics (0-100 scale)
    cost_score = max(0, 100 - cost)
    co2_score = max(0, 100 - (co2 * 5))
    recyc_score = recyclability
    
    sustainability = (
        cost_score * weights["cost"] +
        co2_score * weights["co2"] +
        recyc_score * weights["recyclability"]
    )
    
    return round(max(0, min(100, sustainability)), 2)


def register_prediction_routes(app):

    @app.route("/predict", methods=["POST"])
    def predict():
        data = request.get_json()

        # ----------------------------
        # 1. Check if JSON is provided
        # ----------------------------
        if not data:
            return jsonify({"error": "Request body must be JSON"}), 400

        # ----------------------------
        # 2. Required fields validation
        # ----------------------------
        required_fields = [
            "product_name",
            "product_weight_kg",
            "category",
            "fragility_index",
            "shipping_type"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: {field}"
                }), 400

        # ----------------------------
        # 3. Data type validation
        # ----------------------------
        if not isinstance(data["product_weight_kg"], (int, float)):
            return jsonify({"error": "product_weight_kg must be a number"}), 400

        if not isinstance(data["fragility_index"], (int, float)):
            return jsonify({"error": "fragility_index must be a number between 0 and 1"}), 400

        if not (0 <= data["fragility_index"] <= 1):
            return jsonify({"error": "fragility_index must be between 0 and 1"}), 400

        if data["category"] not in VALID_CATEGORIES:
            return jsonify({"error": "Invalid category value"}), 400

        # ----------------------------
        # 4. ML Model Prediction Logic
        # ----------------------------
        if USE_ML_MODELS:
            try:
                predictions = []
                
                # For each material, create a prediction
                for _, material in materials_df.iterrows():
                    # Create input dataframe with product + material features
                    input_data = pd.DataFrame([{
                        'product_weight': data["product_weight_kg"],
                        'fragility_index': data["fragility_index"],
                        'category': data["category"],
                        'shipping_type': data["shipping_type"],
                        'material_type': material['material_type'],
                        'strength_mpa': material['strength_mpa'],
                        'weight_capacity': material['weight_capacity'],
                        'biodegradability_percent': material['biodegradability_percent'],
                        'co2_emission_score': material['co2_emission_score'],
                        'recyclability_percent': material['recyclability_percent'],
                        'cost_per_kg': material['cost_per_kg']
                    }])
                    
                    # Transform and predict
                    X_transformed = preprocessing_pipeline.transform(input_data)
                    predicted_cost = rf_cost_model.predict(X_transformed)[0]
                    predicted_co2 = xgb_co2_model.predict(X_transformed)[0]
                    
                    # Use advanced ranking if available, otherwise simplified
                    if USE_ADVANCED_RANKING:
                        # Advanced ranking logic from your ranker.py
                        w = ranking_config["weights"]
                        
                        # Min-max normalization within this batch
                        # (In production, you'd normalize across all materials first)
                        cost_norm = 1 - (predicted_cost / 100)  # Inverse: lower cost = better
                        co2_norm = 1 - (predicted_co2 / 50)     # Inverse: lower CO2 = better
                        suit_norm = material['strength_mpa'] / 30  # Higher strength = better
                        
                        ranking_score = (
                            w["cost"] * max(0, cost_norm) +
                            w["co2"] * max(0, co2_norm) +
                            w["suitability"] * max(0, suit_norm)
                        )
                        
                        sustainability = ranking_score * 100
                    else:
                        # Simplified sustainability scoring (backup)
                        sustainability = calculate_simplified_sustainability(
                            predicted_cost, 
                            predicted_co2, 
                            material['recyclability_percent'],
                            data["category"]
                        )
                    
                    predictions.append({
                        "material": material['material_type'],
                        "predicted_cost": round(float(predicted_cost), 2),
                        "co2": round(float(predicted_co2), 2),
                        "sustainability_score": round(float(max(0, min(100, sustainability))), 2)
                    })
                
                # Sort by sustainability score
                predictions.sort(key=lambda x: x["sustainability_score"], reverse=True)
                
                # Apply top_n constraint from config if using advanced ranking
                if USE_ADVANCED_RANKING:
                    top_n = ranking_config.get("top_n", 4)
                    predictions = predictions[:top_n]
                
                # Add ranks
                for idx, pred in enumerate(predictions, 1):
                    pred["rank"] = idx
                
            except Exception as e:
                import traceback
                error_details = traceback.format_exc()
                print(f"❌ ML prediction error: {e}")
                print(error_details)
                return jsonify({"error": f"ML prediction failed: {str(e)}"}), 500
        else:
            # Fallback to mock predictions
            # Top 4 sustainable packaging materials with different properties
            materials_data = [
                {"name": "Recycled Cardboard", "cost_factor": 1.0, "co2_factor": 1.3, "recyclability": 88, "fragility_bonus": 5},
                {"name": "PLA (Polylactic Acid)", "cost_factor": 1.6, "co2_factor": 0.7, "recyclability": 92, "fragility_bonus": 8},
                {"name": "Kraft Paper", "cost_factor": 0.8, "co2_factor": 1.1, "recyclability": 85, "fragility_bonus": 3},
                {"name": "Bio-Plastic (Cornstarch)", "cost_factor": 1.4, "co2_factor": 0.8, "recyclability": 90, "fragility_bonus": 7}
            ]
            
            predictions = []
            
            # Category-specific adjustments
            category_weights = {
                "Food": {"cost": 0.4, "co2": 0.3, "recyclability": 0.3},
                "Electronics": {"cost": 0.3, "co2": 0.2, "recyclability": 0.5},
                "Cosmetics": {"cost": 0.5, "co2": 0.2, "recyclability": 0.3},
                "Pharmacy": {"cost": 0.35, "co2": 0.25, "recyclability": 0.4}
            }
            
            weights = category_weights.get(data["category"], {"cost": 0.33, "co2": 0.33, "recyclability": 0.34})
            
            for idx, mat_info in enumerate(materials_data, 1):
                # Calculate costs based on material properties and product weight
                base_cost = data["product_weight_kg"] * 45 * mat_info["cost_factor"]
                fragility_factor = data["fragility_index"] * (40 - mat_info["fragility_bonus"])
                cost = base_cost + fragility_factor
                
                # Calculate CO2 based on weight, shipping type, and material
                shipping_multiplier = {"Air": 3.5, "Road": 1.5, "Sea": 0.8}.get(data["shipping_type"], 1.5)
                co2 = data["product_weight_kg"] * shipping_multiplier * 2.0 * mat_info["co2_factor"]
                
                # Normalize metrics for scoring (0-100 scale)
                # Lower cost is better, so invert
                cost_score = max(0, 100 - cost)
                # Lower CO2 is better, so invert
                co2_score = max(0, 100 - (co2 * 5))
                # Higher recyclability is better
                recyc_score = mat_info["recyclability"]
                
                # Calculate weighted sustainability score based on category
                sustainability = (
                    cost_score * weights["cost"] +
                    co2_score * weights["co2"] +
                    recyc_score * weights["recyclability"]
                )
                
                predictions.append({
                    "rank": idx,
                    "material": mat_info["name"],
                    "predicted_cost": round(cost, 2),
                    "co2": round(co2, 2),
                    "sustainability_score": round(max(0, min(100, sustainability)), 2)
                })
            
            # Sort by sustainability score (best first)
            predictions.sort(key=lambda x: x["sustainability_score"], reverse=True)
            
            # Re-rank after sorting
            for idx, pred in enumerate(predictions, 1):
                pred["rank"] = idx

        # ----------------------------
        # 5. Return response
        # ----------------------------
        return jsonify({
            "predictions": predictions,
            "model_version": "v1.0",
            "status": "success"
        }), 200
