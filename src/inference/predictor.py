import joblib
import pandas as pd

class Predictor:
    def __init__(self, model_path="ml/models/rf_cost.joblib"):
        self.model = joblib.load(model_path)
        self.expected_features = list(self.model.feature_names_in_)

    def predict(self, data):
        df = pd.DataFrame([data])

        # 🧠 Inject realistic defaults for missing features
        defaults = {
            "CEI": 0.6,
            "CII": 0.4,
            "MSS": 0.7,
            "strength_mpa": 30,
            "weight_capacity": 15,
            "biodegradability_percent": 45,
            "recyclability_percent": 70,
            "industry_use_case": "General",
            "material_type": "Paper/Bio-Based"
        }

        for col in self.expected_features:
            if col not in df.columns:
                df[col] = defaults.get(col, 0)

        # Force categorical columns to string
        for col in ["category", "shipping_type", "industry_use_case", "material_type"]:
            if col in df.columns:
                df[col] = df[col].astype(str)

        # Ensure correct order
        df = df[self.expected_features]

        prediction = self.model.predict(df)
        return float(prediction[0])


