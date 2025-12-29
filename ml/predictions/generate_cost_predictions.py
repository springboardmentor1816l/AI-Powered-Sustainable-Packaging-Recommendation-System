import pandas as pd
import joblib
import os

# -----------------------------
# PATHS
# -----------------------------
X_PATH = "data/final/X_raw.csv"
MODEL_PATH = "ml/models/rf_cost_model_v1.pkl"
OUTPUT_DIR = "ml/metrics"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "rf_cost_predictions.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# LOAD DATA & MODEL
# -----------------------------
X = pd.read_csv(X_PATH)
model = joblib.load(MODEL_PATH)

# -----------------------------
# ENCODE FEATURES (same as training)
# -----------------------------
X_encoded = pd.get_dummies(X, drop_first=True)

# -----------------------------
# PREDICT
# -----------------------------
predictions = model.predict(X_encoded)

# -----------------------------
# SAVE
# -----------------------------
pd.DataFrame({
    "predicted_cost": predictions
}).to_csv(OUTPUT_PATH, index=False)

print("✅ RF cost predictions saved at:", OUTPUT_PATH)
