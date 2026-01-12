import joblib
import pandas as pd

class EcoPackPredictor:
    def __init__(self, pipeline_path, cost_model_path, co2_model_path):
        # Module 4 Artifacts
        self.pipeline = joblib.load(pipeline_path)
        self.cost_model = joblib.load(cost_model_path)
        self.co2_model = joblib.load(co2_model_path)
        
        # Map expected features to prevent "Missing Column" errors
        self.required_columns = self.pipeline.feature_names_in_

    def predict(self, raw_data_df):
        # Create template to match training schema
        full_input = pd.DataFrame(0, index=range(len(raw_data_df)), columns=self.required_columns)
        
        for col in raw_data_df.columns:
            if col in full_input.columns:
                full_input[col] = raw_data_df[col]
        
        # Transform using your Module 2 Preprocessing Pipeline
        X_transformed = self.pipeline.transform(full_input)
        
        return {
            'cost_index': self.cost_model.predict(X_transformed).tolist(),
            'co2_impact': self.co2_model.predict(X_transformed).tolist()
        }