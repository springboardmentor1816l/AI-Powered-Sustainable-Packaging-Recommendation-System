import pandas as pd
import joblib
import os

# -----------------------------
# PATHS
# -----------------------------
X_PATH = "data/final/X_raw.csv"
MATERIAL_PATH = "data/processed/material_cleaned.csv"
MODEL_PATH = "ml/models/xgb_co2_model_v1.joblib"

OUTPUT_DIR = "ml/metrics"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "xgb_co2_predictions.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
X = pd.read_csv(X_PATH)
materials = pd.read_csv(MATERIAL_PATH)
model = joblib.load(MODEL_PATH)

# -----------------------------
# CREATE CO2 TARGET FEATURES
# -----------------------------
X_features = X.drop(columns=["material_type"])
X_encoded = pd.get_dummies(X_features, drop_first=True)

# -----------------------------
# PREDICT
# -----------------------------
predictions = model.predict(X_encoded)

# -----------------------------
# SAVE
# -----------------------------
pd.DataFrame({
    "predicted_co2": predictions
}).to_csv(OUTPUT_PATH, index=False)

print("✅ CO₂ predictions saved at:", OUTPUT_PATH)
