import pandas as pd
import joblib
from pathlib import Path


# -----------------------------
# Paths
# -----------------------------
PREPROCESSOR_PATH = "models/preprocessing/co2_preprocessing_pipeline.pkl"

COST_MODEL_PATH = "ml/models/rf_cost.joblib"
CO2_MODEL_PATH = "ml/models/xgb_co2.joblib"


# -----------------------------
# Load artifacts (ONCE)
# -----------------------------
print("🔹 Loading preprocessing pipeline and models...")

preprocessor = joblib.load(PREPROCESSOR_PATH)
cost_model = joblib.load(COST_MODEL_PATH)
co2_model = joblib.load(CO2_MODEL_PATH)

print("✅ Models loaded successfully")


# -----------------------------
# Predictor Class
# -----------------------------
class EcoPackPredictor:
    """
    Unified inference interface for EcoPackAI.
    Predicts:
    - Cost per unit
    - CO₂ emission per unit
    """

    def __init__(self):
        self.preprocessor = preprocessor
        self.cost_model = cost_model
        self.co2_model = co2_model

    def predict(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Batch prediction
        Input:
            X -> DataFrame with feature columns
        Output:
            DataFrame with predictions
        """

        # -----------------------------
        # Preprocess
        # -----------------------------
        X_processed = self.preprocessor.transform(X)

        # -----------------------------
        # Predict
        # -----------------------------
        cost_pred = self.cost_model.predict(X_processed)
        co2_pred = self.co2_model.predict(X_processed)

        # -----------------------------
        # Output
        # -----------------------------
        results = X.copy()
        results["predicted_cost_per_unit"] = cost_pred
        results["predicted_co2_per_unit"] = co2_pred

        return results

    def predict_single(self, sample: dict) -> dict:
        """
        Single record prediction
        Input:
            sample -> dict of features
        Output:
            dict with predictions
        """

        df = pd.DataFrame([sample])
        result = self.predict(df).iloc[0]

        return {
            "predicted_cost_per_unit": float(result["predicted_cost_per_unit"]),
            "predicted_co2_per_unit": float(result["predicted_co2_per_unit"])
        }


# -----------------------------
# Example usage (CLI test)
# -----------------------------
if __name__ == "__main__":
    predictor = EcoPackPredictor()

    sample_input = {
        "product_weight_kg": 1.2,
        "fragility_index": 3,
        "shipping_type": "Road",
        "category": "Food",
        "packaging_type": "Box",
        "recyclability_pct": 85,
        "load_handling_score": 7,
        "moisture_resistance_score": 6,
        "thermal_resistance_score": 5,
        "supplier_sustainability_compliance_pct": 90,
        "sustainability_target_progress_pct": 88
    }

    prediction = predictor.predict_single(sample_input)
    print("\n📦 Sample Prediction:")
    print(prediction)
