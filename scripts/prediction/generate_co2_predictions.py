import pandas as pd
import joblib
from pathlib import Path

# -------------------------
# PATHS
# -------------------------
X_RAW_PATH = "data/model_inputs/X_raw.csv"
PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
MODEL_PATH = "ml/models/xgb/xgb_co2_v1.joblib"
OUT_PATH = "data/predictions/co2_predictions.csv"

Path("data/predictions").mkdir(parents=True, exist_ok=True)

# -------------------------
# LOAD DATA
# -------------------------
print("Loading X_raw...")
X = pd.read_csv(X_RAW_PATH)

print("Loading preprocessing pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)

print("Loading CO₂ model...")
co2_model = joblib.load(MODEL_PATH)

# -------------------------
# TRANSFORM FEATURES
# -------------------------
print("Applying preprocessing...")
X_transformed = preprocessor.transform(X)

# -------------------------
# PREDICT CO₂
# -------------------------
print("Predicting CO₂ emissions...")
predicted_co2 = co2_model.predict(X_transformed)

# -------------------------
# SAVE OUTPUT
# -------------------------
output = X.copy()
output["predicted_co2"] = predicted_co2

output.to_csv(OUT_PATH, index=False)

print("✅ CO₂ predictions generated")
print(f"Saved to → {OUT_PATH}")
