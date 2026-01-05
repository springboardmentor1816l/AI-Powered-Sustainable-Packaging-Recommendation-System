import pandas as pd
import joblib
import numpy as np
from pathlib import Path

class Predictor:
    def __init__(self, model_path="ml/models/rf_cost_pipeline.joblib"):
        # Load the model once when the class is initialized
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(self, data):
        import pandas as pd
        
        # 1. Create the DataFrame from your sample
        df = pd.DataFrame([data])
        
        # 2. RUN PREPROCESSING FIRST (This is the key!)
        # Instead of manually filling 0s, we let the pipeline transform the words
        try:
            # If your model is a Pipeline, it has the 'preprocessing' step built-in
            # We want to transform the raw dictionary into the model's numeric format
            transformed_data = self.model.named_steps['preprocessing'].transform(df)
            
            # 3. Predict using the transformed numeric data
            prediction = self.model.predict(df) # Pipelines usually handle df directly
        except Exception as e:
            # If the above fails, your pipeline might be set up differently.
            # Let's use the safer alignment method:
            expected_features = self.model.feature_names_in_
            for col in expected_features:
                if col not in df.columns:
                    df[col] = 0
            df = df[expected_features]
            prediction = self.model.predict(df)
            
        return prediction[0]