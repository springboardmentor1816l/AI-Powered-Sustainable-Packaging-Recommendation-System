import pandas as pd
import os

# -----------------------------
# PATHS
# -----------------------------
INTEGRATED_PATH = "data/engineered/integrated_with_suitability.csv"
COST_PRED_PATH = "data/predictions/cost_predictions.csv"
CO2_PRED_PATH = "data/predictions/co2_predictions.csv"

OUT_PATH = "data/final/final_ranking_dataset.csv"

os.makedirs("data/final", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
print("Loading integrated dataset...")
df = pd.read_csv(INTEGRATED_PATH)

print("Loading cost predictions...")
cost_df = pd.read_csv(COST_PRED_PATH)

print("Loading CO₂ predictions...")
co2_df = pd.read_csv(CO2_PRED_PATH)

# -----------------------------
# VALIDATION CHECK
# -----------------------------
assert len(df) == len(cost_df) == len(co2_df), \
    "Row mismatch between datasets!"

# -----------------------------
# ADD PREDICTIONS
# -----------------------------
df["predicted_cost"] = cost_df["predicted_cost"]
df["predicted_co2"] = co2_df["predicted_co2"]

# -----------------------------
# FINAL COLUMN CHECK
# -----------------------------
required_cols = {
    "predicted_cost",
    "predicted_co2",
    "Material Suitability Score"
}

missing = required_cols - set(df.columns)
if missing:
    raise ValueError(f"Missing required columns: {missing}")

# -----------------------------
# SAVE FINAL DATASET
# -----------------------------
df.to_csv(OUT_PATH, index=False)

print("✅ Final ranking dataset created successfully")
print(f"Saved to → {OUT_PATH}")
print(f"Final shape: {df.shape}")
