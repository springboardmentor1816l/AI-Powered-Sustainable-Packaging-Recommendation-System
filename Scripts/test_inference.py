import sys
import joblib
from pathlib import Path

# Setup Pathing
root_path = Path(__file__).resolve().parents[1]
sys.path.append(str(root_path))

from src.inference.predictor import Predictor

def main():
    # Initialize the prediction engine
    engine = Predictor()

    # Organized Sample Data
    sample = {
        # Identifiers
        "product_id": "0",
        "product_name": "Unknown",
        "material_id": "0",

        # Product Specs
        "product_weight": 0.4,
        "fragility_index": 3,
        "category": "Electronics",
        "shipping_type": "Standard",
        "industry_use_case": "Retail",

        # Material Attributes
        "material_type": "Plastic",
        "strength_mpa": 0.7,
        "weight_capacity": 0.6,
        "biodegradability_percent": 0.2,
        "recyclability_percent": 0.5,

        # Sustainability Indices
        "CII": 0.5,  # Carbon Intensity Index
        "CEI": 0.5,  # Circular Economy Index
        "MSS": 0.5   # Material Sustainability Score
    }

    # Execute Prediction
    try:
        out = engine.predict(sample)
        print("-" * 30)
        print(f"RESULT PREDICTION: {out:.4f}")
        print("-" * 30)
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

    print("Process Complete. DONE")

if __name__ == "__main__":
    main()