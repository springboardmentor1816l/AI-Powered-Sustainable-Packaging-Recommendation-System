import os

API_KEY = os.getenv("PACKAGING_API_KEY", "supersecret123")

VALID_PAYLOAD = {
    "material_type": "plastic",
    "industry_use_case": "food",
    "source_type": "recycled",
    "weight_capacity_kg": 2.0,
    "strength_mpa": 30,
    "recyclability_percent": 70,
    "biodegradability_percent": 20,
    "co2_emission_kg_per_kg": 1.2,
    "co2_impact_index": 0.5,
    "cost_efficiency_index": 0.8,
    "recyclability_category": "high"
}
