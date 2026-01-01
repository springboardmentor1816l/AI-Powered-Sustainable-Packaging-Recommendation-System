import joblib
import pandas as pd
import numpy as np

class EcoPackPredictor:
    def __init__(self, pipeline_path, cost_model_path, co2_model_path):
        self.pipeline = joblib.load(pipeline_path)
        self.cost_model = joblib.load(cost_model_path)
        self.co2_model = joblib.load(co2_model_path)
        
        # Define the attributes the API expects to see
        self.required_input_columns = self.pipeline.feature_names_in_
        self.expected_features = list(self.cost_model.feature_names_in_)

    def predict(self, raw_data_df):
        # Create full template to avoid missing column errors
        full_input = pd.DataFrame(0, index=range(len(raw_data_df)), columns=self.required_input_columns)
        
        # Overwrite with user-provided values
        for col in raw_data_df.columns:
            if col in full_input.columns:
                full_input[col] = raw_data_df[col]
        
        # Preprocessing & Model Alignment
        X_transformed = self.pipeline.transform(full_input)
        all_features = self.pipeline.get_feature_names_out()
        clean_names = [name.split('__')[-1] for name in all_features]
        X_df = pd.DataFrame(X_transformed, columns=clean_names)
        
        # Select only the features the model was trained on
        X_final = X_df[self.expected_features]
        
        return {
            'cost_index': self.cost_model.predict(X_final).tolist(),
            'co2_impact': self.co2_model.predict(X_final).tolist()
        }