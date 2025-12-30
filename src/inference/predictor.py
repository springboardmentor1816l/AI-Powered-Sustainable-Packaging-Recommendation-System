import joblib
import pandas as pd
import numpy as np

class EcoPackPredictor:
    """Unified inference entry point for EcoPackAI models."""
    def __init__(self, pipeline_path, cost_model_path, co2_model_path):
        self.pipeline = joblib.load(pipeline_path)
        self.cost_model = joblib.load(cost_model_path)
        self.co2_model = joblib.load(co2_model_path)
        self.expected_features = list(self.cost_model.feature_names_in_)

    def predict(self, raw_df):
        # 1. Preprocess
        X_trans = self.pipeline.transform(raw_df)
        
        # 2. Align Feature Names (strip pipeline prefixes)
        feature_names = [n.split('__')[-1] for n in self.pipeline.get_feature_names_out()]
        X_df = pd.DataFrame(X_trans, columns=feature_names)
        
        # 3. Handle missing expected features (fill leaky/missing with 0)
        for col in self.expected_features:
            if col not in X_df.columns:
                X_df[col] = 0
        
        # 4. Predict
        X_final = X_df[self.expected_features]
        return {
            'cost_index': self.cost_model.predict(X_final),
            'co2_impact': self.co2_model.predict(X_final)
        }
