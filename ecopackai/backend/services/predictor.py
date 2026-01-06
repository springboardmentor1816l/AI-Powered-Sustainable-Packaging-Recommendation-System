import pandas as pd
import joblib

cost_model = joblib.load("backend/models/cost_impact_model.pkl")
co2_model  = joblib.load("backend/models/co2_impact_model.pkl")

FEATURES = list(cost_model.feature_names_in_)

def build_features(data):
    """Convert minimal input into full feature vector"""

    row = {
        # user inputs
        "category": data["category"],
        "shipping_type": data["shipping_type"],
        "material_type": data["material_type"],
        "packaging_type": data["packaging_type"],
        "supplier_region": data["supplier_region"],
        "product_weight_kg": data["product_weight_kg"],
        "fragility_index": data["fragility_index"],

        # engineered defaults (VERY IMPORTANT)
        "biodegradation_time_days": 180,
        "load_handling_score": data["fragility_index"] * 10,
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

    # Encode categoricals
    for col in X.select_dtypes(include="object").columns:
        X[col] = X[col].astype("category").cat.codes

    return X


def predict_scores(data):
    X = build_features(data)

    cost_proba = cost_model.predict_proba(X)
    co2_proba  = co2_model.predict_proba(X)

    cost_score = float(0.2 * cost_proba[:,0] + 0.5 * cost_proba[:,1] + 0.3 * cost_proba[:,2])
    co2_score  = float(0.2 * co2_proba[:,0]  + 0.5 * co2_proba[:,1]  + 0.3 * co2_proba[:,2])

    sustainability_score = round((1 - cost_score) * (1 - co2_score), 3)

    return {
        "cost_impact_score": round(cost_score, 3),
        "co2_impact_score": round(co2_score, 3),
        "final_sustainability_score": sustainability_score
    }


