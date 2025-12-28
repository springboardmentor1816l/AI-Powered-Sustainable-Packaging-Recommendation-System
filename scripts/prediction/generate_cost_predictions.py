import pandas as pd
import joblib
from pathlib import Path

# -------------------------
# PATHS
# -------------------------
X_RAW_PATH = "data/model_inputs/X_raw.csv"
PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
MODEL_PATH = "ml/models/rf/rf_cost_v1.joblib"
OUT_PATH = "data/predictions/cost_predictions.csv"

Path("data/predictions").mkdir(parents=True, exist_ok=True)

# -------------------------
# LOAD DATA
# -------------------------
print("Loading X_raw features...")
X = pd.read_csv(X_RAW_PATH)

print("Loading preprocessing pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)

print("Loading trained cost model...")
cost_model = joblib.load(MODEL_PATH)

# -------------------------
# TRANSFORM FEATURES
# -------------------------
print("Applying preprocessing...")
X_transformed = preprocessor.transform(X)

# -------------------------
# PREDICT COST
# -------------------------
print("Generating cost predictions...")
predicted_cost = cost_model.predict(X_transformed)

# -------------------------
# SAVE OUTPUT
# -------------------------
output = X.copy()
output["predicted_cost"] = predicted_cost

output.to_csv(OUT_PATH, index=False)

print("✅ Cost predictions generated successfully")
print(f"Saved to → {OUT_PATH}")
