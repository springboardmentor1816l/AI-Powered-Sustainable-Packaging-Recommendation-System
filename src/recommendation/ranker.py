import pandas as pd
import yaml
from sklearn.preprocessing import MinMaxScaler
import os

# =====================================================
# LOAD CONFIG
# =====================================================
with open("config/ranking_weights.yaml", "r") as f:
    config = yaml.safe_load(f)

W = config["weights"]
C = config["constraints"]

# =====================================================
# LOAD DATA
# =====================================================
DATA_PATH = "data/final/X_raw.csv"
COST_PRED_PATH = "ml/metrics/rf_cost_predictions.csv"
CO2_PRED_PATH = "ml/metrics/xgb_co2_predictions.csv"

df = pd.read_csv(DATA_PATH)

df["predicted_cost"] = pd.read_csv(COST_PRED_PATH)["predicted_cost"]
df["predicted_co2"] = pd.read_csv(CO2_PRED_PATH)["predicted_co2"]

print("Initial data shape:", df.shape)

# =====================================================
# CREATE MATERIAL SUITABILITY SCORE
# =====================================================
df["material_suitability_score"] = (
    0.4 * df["strength_mpa"] +
    0.3 * df["weight_capacity"] +
    0.3 * df["biodegradability_percent"]
)

print("✅ Material suitability score computed")

# =====================================================
# APPLY CONSTRAINTS
# =====================================================
df = df[
    (df["recyclability_percent"] >= C["min_recyclability_percent"]) &
    (df["predicted_cost"] <= C["max_cost_per_kg"])
].copy()

print("After constraints shape:", df.shape)

# =====================================================
# NORMALIZATION
# =====================================================
scaler = MinMaxScaler()

df["cost_norm"] = scaler.fit_transform(df[["predicted_cost"]])
df["co2_norm"] = scaler.fit_transform(df[["predicted_co2"]])
df["suitability_norm"] = scaler.fit_transform(df[["material_suitability_score"]])
df["recyclability_norm"] = scaler.fit_transform(df[["recyclability_percent"]])

# =====================================================
# FINAL COMPOSITE SCORE
# =====================================================
df["final_score"] = (
    W["cost"] * (1 - df["cost_norm"]) +
    W["co2"] * (1 - df["co2_norm"]) +
    W["suitability"] * df["suitability_norm"] +
    W["recyclability"] * df["recyclability_norm"]
)

# =====================================================
# GLOBAL RANKING (NO product_id)
# =====================================================
df["rank"] = df["final_score"].rank(method="dense", ascending=False)

# =====================================================
# SAVE OUTPUT
# =====================================================
os.makedirs("outputs", exist_ok=True)

OUTPUT_PATH = "outputs/material_rankings.csv"
df.sort_values("rank").to_csv(OUTPUT_PATH, index=False)

print("✅ Global material ranking completed successfully")
print("📁 Output saved at:", OUTPUT_PATH)
