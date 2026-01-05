from src.inference.predictor import MaterialSuitabilityPredictor
import pandas as pd

# Load real test input schema
X_test = pd.read_parquet("data/model_inputs/X_test.parquet")

# Take one real sample
sample_input = X_test.iloc[[0]]

# Initialize predictor
predictor = MaterialSuitabilityPredictor()

# Predict
prediction = predictor.predict(sample_input)

print("✅ Prediction:", prediction)
