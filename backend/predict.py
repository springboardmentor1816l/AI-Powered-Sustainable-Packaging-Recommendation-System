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


def calculate_sustainability_score(biodegradability, recyclability, is_renewable=True):
    """
    Calculate Sustainability Score based on:
    - Biodegradability (40%)
    - Recyclability (40%)
    - Renewable resources (20%)
    
    All inputs should be on 0-100 scale.
    """
    renewability_score = 80 if is_renewable else 20  # Bio-based materials get higher score
    
    sustainability_score = (
        biodegradability * 0.40 +      # 40% weight
        recyclability * 0.40 +          # 40% weight
        renewability_score * 0.20       # 20% weight
    )
    
    return round(max(0, min(100, sustainability_score)), 2)


def calculate_co2_performance_score(co2_emissions, max_co2=50):
    """
    Calculate CO2 Performance Score.
    Lower emissions = Higher score (inverted scale).
    
    Score = 100 - (emissions / max_emissions * 100)
    """
    co2_score = 100 - (co2_emissions / max_co2 * 100)
    return round(max(0, min(100, co2_score)), 2)


def calculate_final_ranking_score(sustainability_score, co2_performance_score, alpha=0.6, beta=0.4):
    """
    Composite Score Calculation:
    Final Score = alpha * Sustainability Score + beta * CO2 Performance Score
    
    Default weights: Sustainability (60%) > CO2 Impact (40%)
    This ensures sustainability is prioritized over CO2 impact.
    """
    final_score = (alpha * sustainability_score) + (beta * co2_performance_score)
    return round(max(0, min(100, final_score)), 2)


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

        if data["shipping_type"] not in VALID_SHIPPING:
            return jsonify({"error": "Invalid shipping_type value"}), 400

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
            # =====================================================
            # RANKING LOGIC: CO2 Impact & Sustainability
            # =====================================================
            # EcoPackAI ranks packaging materials by evaluating how well 
            # each material minimizes CO2 impact while maximizing sustainability,
            # based on the product's physical and logistical requirements.
            
            # === MATERIAL DATABASE ===
            # Packaging materials with comprehensive properties
            materials_data = [
                {
                    "name": "Recycled Cardboard", 
                    "base_co2_per_kg": 1.3,        # kg CO2 per kg material
                    "recyclability": 88,           # 0-100 scale
                    "biodegradability": 85,        # 0-100 scale
                    "is_renewable": True,          # From renewable resources
                    "strength_factor": 0.7,        # Thickness multiplier for strength
                    "max_weight": 15,              # kg capacity
                    "fragility_protection": 6,     # Protection level 1-10
                    "shipping_suitability": {"Air": 0.9, "Road": 1.0, "Sea": 0.95},
                    "category_bonus": {"Food": 1.1, "Electronics": 0.9, "Cosmetics": 0.95, "Pharmacy": 0.9}
                },
                {
                    "name": "PLA (Polylactic Acid)", 
                    "base_co2_per_kg": 0.7,
                    "recyclability": 92, 
                    "biodegradability": 95,
                    "is_renewable": True,
                    "strength_factor": 0.85,
                    "max_weight": 10,
                    "fragility_protection": 8,
                    "shipping_suitability": {"Air": 1.0, "Road": 0.95, "Sea": 0.7},
                    "category_bonus": {"Food": 1.0, "Electronics": 1.1, "Cosmetics": 1.15, "Pharmacy": 1.1}
                },
                {
                    "name": "Kraft Paper", 
                    "base_co2_per_kg": 1.1,
                    "recyclability": 85, 
                    "biodegradability": 90,
                    "is_renewable": True,
                    "strength_factor": 0.5,
                    "max_weight": 8,
                    "fragility_protection": 4,
                    "shipping_suitability": {"Air": 0.7, "Road": 1.0, "Sea": 0.9},
                    "category_bonus": {"Food": 1.05, "Electronics": 0.7, "Cosmetics": 1.0, "Pharmacy": 0.9}
                },
                {
                    "name": "Bio-Plastic (Cornstarch)", 
                    "base_co2_per_kg": 0.8,
                    "recyclability": 90, 
                    "biodegradability": 98,
                    "is_renewable": True,
                    "strength_factor": 0.8,
                    "max_weight": 12,
                    "fragility_protection": 7,
                    "shipping_suitability": {"Air": 0.95, "Road": 1.0, "Sea": 0.9},
                    "category_bonus": {"Food": 1.15, "Electronics": 1.0, "Cosmetics": 1.1, "Pharmacy": 1.2}
                },
                {
                    "name": "Mushroom Packaging",
                    "base_co2_per_kg": 0.4,
                    "recyclability": 75,
                    "biodegradability": 100,
                    "is_renewable": True,
                    "strength_factor": 0.6,
                    "max_weight": 7,
                    "fragility_protection": 9,
                    "shipping_suitability": {"Air": 0.8, "Road": 0.95, "Sea": 0.6},
                    "category_bonus": {"Food": 0.9, "Electronics": 1.2, "Cosmetics": 1.0, "Pharmacy": 0.95}
                },
                {
                    "name": "Bagasse (Sugarcane Fiber)",
                    "base_co2_per_kg": 0.5,
                    "recyclability": 80,
                    "biodegradability": 95,
                    "is_renewable": True,
                    "strength_factor": 0.55,
                    "max_weight": 6,
                    "fragility_protection": 5,
                    "shipping_suitability": {"Air": 0.75, "Road": 1.0, "Sea": 0.85},
                    "category_bonus": {"Food": 1.2, "Electronics": 0.8, "Cosmetics": 1.0, "Pharmacy": 1.0}
                }
            ]
            
            # =====================================================
            # STEP 1: FEASIBILITY CHECK
            # =====================================================
            # Filter materials based on product requirements
            feasible_materials = []
            
            for mat in materials_data:
                # 1a. Weight Capacity Check
                if data["product_weight_kg"] > mat["max_weight"]:
                    continue
                
                # 1b. Fragility Protection Check
                # High fragility (>0.7) requires protection level >= 6
                # Medium fragility (0.4-0.7) requires protection level >= 4
                required_protection = 6 if data["fragility_index"] > 0.7 else (4 if data["fragility_index"] > 0.4 else 2)
                if mat["fragility_protection"] < required_protection:
                    continue
                
                # 1c. Shipping Type Suitability Check
                shipping_suitability = mat["shipping_suitability"].get(data["shipping_type"], 0)
                if shipping_suitability < 0.7:  # Below 70% suitability = not feasible
                    continue
                
                feasible_materials.append(mat)
            
            # Fallback: If no materials pass, include all with reduced scores
            if not feasible_materials:
                feasible_materials = materials_data
                print("Warning: No materials meet all feasibility criteria. Showing all options.")
            
            # =====================================================
            # STEP 2 & 3: CO2 ESTIMATION & SUSTAINABILITY SCORING
            # =====================================================
            predictions = []
            
            for mat in feasible_materials:
                # ---------------------------------------------------
                # 2a. Calculate Required Material Thickness
                # ---------------------------------------------------
                # Thickness based on weight and fragility requirements
                base_thickness = 1.0  # Base thickness in relative units
                weight_factor = 1 + (data["product_weight_kg"] / mat["max_weight"]) * 0.5
                fragility_factor = 1 + (data["fragility_index"] * mat["strength_factor"])
                required_thickness = base_thickness * weight_factor * fragility_factor
                
                # ---------------------------------------------------
                # 2b. CO2 Impact Estimation
                # ---------------------------------------------------
                # CO2 = base_emission * weight * thickness * shipping_multiplier
                shipping_emission_multiplier = {
                    "Air": 3.5,      # Highest emissions (air freight)
                    "Road": 1.5,     # Medium emissions (truck)
                    "Sea": 0.8       # Lowest emissions (ship)
                }.get(data["shipping_type"], 1.5)
                
                co2_emissions = (
                    mat["base_co2_per_kg"] * 
                    data["product_weight_kg"] * 
                    required_thickness * 
                    shipping_emission_multiplier
                )
                
                # ---------------------------------------------------
                # 2c. Predicted Cost Calculation
                # ---------------------------------------------------
                base_cost_per_kg = 45  # Base cost in Rs.
                cost = (
                    base_cost_per_kg * 
                    data["product_weight_kg"] * 
                    required_thickness * 
                    (1 / mat["strength_factor"])  # Stronger materials = less material needed
                )
                
                # ---------------------------------------------------
                # 3a. Sustainability Score Calculation
                # ---------------------------------------------------
                # Biodegradability (40%) + Recyclability (40%) + Renewability (20%)
                category_modifier = mat["category_bonus"].get(data["category"], 1.0)
                
                adjusted_biodegradability = min(100, mat["biodegradability"] * category_modifier)
                adjusted_recyclability = min(100, mat["recyclability"] * category_modifier)
                
                sustainability_score = calculate_sustainability_score(
                    adjusted_biodegradability,
                    adjusted_recyclability,
                    mat["is_renewable"]
                )
                
                # ---------------------------------------------------
                # 3b. CO2 Performance Score
                # ---------------------------------------------------
                # Lower emissions = Higher score
                co2_performance_score = calculate_co2_performance_score(co2_emissions, max_co2=50)
                
                # =====================================================
                # STEP 4: COMPOSITE SCORE CALCULATION
                # =====================================================
                # Final Score = alpha(Sustainability) + beta(CO2 Performance)
                # Sustainability is prioritized: alpha=0.6, beta=0.4
                final_score = calculate_final_ranking_score(
                    sustainability_score,
                    co2_performance_score,
                    alpha=0.6,  # Sustainability weight (60%)
                    beta=0.4    # CO2 impact weight (40%)
                )
                
                predictions.append({
                    "rank": 0,
                    "material": mat["name"],
                    "predicted_cost": round(cost, 2),
                    "co2": round(co2_emissions, 2),
                    "sustainability_score": final_score,
                    # Additional metrics for transparency
                    "biodegradability": mat["biodegradability"],
                    "recyclability": mat["recyclability"],
                    "co2_performance": co2_performance_score
                })
            
            # =====================================================
            # STEP 5: FINAL RANKING
            # =====================================================
            # Sort by Final Score (descending) - highest score = Rank #1
            predictions.sort(key=lambda x: x["sustainability_score"], reverse=True)
            
            # Assign ranks
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
