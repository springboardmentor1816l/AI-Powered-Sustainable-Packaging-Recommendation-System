import joblib
import pandas as pd
import numpy as np

# paths
MODEL_PATH = "ml/models/xgb_co2_model.pkl"
DATA_PATH = "data/final/co2_features.csv"

# load model
model = joblib.load(MODEL_PATH)
print("✅ CO2 model loaded successfully")

# load some data
df = pd.read_csv(DATA_PATH)

X = df.drop(columns=["co2_emission"])
y = df["co2_emission"]

# predict on first 5 rows
preds = model.predict(X.head())

print("\n🔹 Sample Predictions vs Actual:")
for i in range(5):
    print(f"Predicted: {preds[i]:.3f} | Actual: {y.iloc[i]:.3f}")
