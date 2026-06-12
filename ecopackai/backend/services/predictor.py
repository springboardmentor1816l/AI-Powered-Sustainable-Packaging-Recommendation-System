import pandas as pd
import joblib

# ===============================
# Load models
# ===============================
cost_model = joblib.load("backend/models/cost_impact_model.pkl")
co2_model  = joblib.load("backend/models/co2_impact_model.pkl")

FEATURES = list(cost_model.feature_names_in_)

# ===============================
# Feature Builder
# ===============================
def build_features(data):
    row = {
        # user inputs
        "category": data["category"],
        "shipping_type": data["shipping_type"],
        "material_type": data["material_type"],
        "packaging_type": data["packaging_type"],
        "supplier_region": data["supplier_region"],
        "product_weight_kg": float(data["product_weight_kg"]),
        "fragility_index": float(data["fragility_index"]),

        # engineered defaults
        "biodegradation_time_days": 180,
        "load_handling_score": float(data["fragility_index"]) * 10,
        "material_suitability_score": 8,
        "moisture_resistance_score": 7,
        "recycled_content_percent": 40,
        "reusability_percent": 50,
        "strength_index": 7,
        "carbon_offset_score": 6,
        "supply_chain_risk": 4,
        "energy_consumption_score": 5,
        "waste_generation_score": 6,
        "transport_efficiency": 7,
        "eco_certification_score": 6,
        "toxicity_score": 3,
        "end_of_life_score": 7,
        "water_usage_score": 5
    }

    X = pd.DataFrame([row])[FEATURES]

    # Encode categoricals (same strategy as training)
    for col in X.select_dtypes(include="object").columns:
        X[col] = X[col].astype("category").cat.codes

    return X


# ===============================
# Prediction Logic (FINAL)
# ===============================
def predict_scores(data):
    # 🔴 DEBUG PRINT (VERY IMPORTANT)
    print("🚨 DEBUG: predictor.py CALLED with input:", data)

    X = build_features(data)

    # Predict probabilities
    cost_proba = cost_model.predict_proba(X)[0]
    co2_proba  = co2_model.predict_proba(X)[0]

    # Impact scores (higher = worse)
    cost_impact_score = float(
        0.2 * cost_proba[0] +
        0.5 * cost_proba[1] +
        0.3 * cost_proba[2]
    )

    co2_impact_score = float(
        0.2 * co2_proba[0] +
        0.5 * co2_proba[1] +
        0.3 * co2_proba[2]
    )

    # Convert to goodness (higher = better)
    cost_goodness = 1 - cost_impact_score
    co2_goodness  = 1 - co2_impact_score

    # 🌱 Base sustainability (environment-first)
    final_sustainability_score = (
        0.7 * co2_goodness +
        0.3 * cost_goodness
    )

    # ===============================
    # 🚚 STRONG WORST-CASE PENALTIES
    # ===============================
    penalty = 0.0

    if data["shipping_type"] == "Air":
        penalty += 0.25   # Air freight is very unsustainable

    if data["supplier_region"] in ["Europe", "North America"]:
        penalty += 0.15   # Long-distance logistics

    if float(data["product_weight_kg"]) > 5:
        penalty += 0.10   # Heavy product

    if float(data["fragility_index"]) > 0.7:
        penalty += 0.10   # Extra protective packaging

    final_sustainability_score -= penalty

    # Clamp to [0, 1]
    final_sustainability_score = max(0, min(1, final_sustainability_score))

    # ===============================
    # Return response
    # ===============================
    return {
        "cost_impact_score": round(cost_impact_score, 3),
        "co2_impact_score": round(co2_impact_score, 3),
        "final_sustainability_score": round(final_sustainability_score, 3)
    }


