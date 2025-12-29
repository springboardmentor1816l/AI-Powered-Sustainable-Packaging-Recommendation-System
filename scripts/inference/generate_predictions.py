import pandas as pd
import joblib
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
DATA_PATH = Path("../../data/integrated/integrated_dataset.csv")
X_PATH = Path("../../data/model_input/X_raw.csv")

PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")
COST_MODEL_PATH = Path("../../ml/models/rf_cost.joblib")
CO2_MODEL_PATH = Path("../../ml/models/xgb_co2.joblib")

OUT_PATH = Path("../../data/integrated/integrated_with_predictions.csv")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
df = pd.read_csv(DATA_PATH)
X_raw = pd.read_csv(X_PATH)

# -------------------------------------------------
# Load models
# -------------------------------------------------
preprocessor = joblib.load(PREPROCESSOR_PATH)
cost_model = joblib.load(COST_MODEL_PATH)
co2_model = joblib.load(CO2_MODEL_PATH)

# -------------------------------------------------
# Transform features
# -------------------------------------------------
X_processed = preprocessor.transform(X_raw)

# -------------------------------------------------
# Predict
# -------------------------------------------------
df["predicted_cost"] = cost_model.predict(X_processed)
df["predicted_co2"] = co2_model.predict(X_processed)

# -------------------------------------------------
# Save
# -------------------------------------------------
df.to_csv(OUT_PATH, index=False)

print("Predictions generated:")
print(" - predicted_cost")
print(" - predicted_co2")
print("Saved to:", OUT_PATH)
