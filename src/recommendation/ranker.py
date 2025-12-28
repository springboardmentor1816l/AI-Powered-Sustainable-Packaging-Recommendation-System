import pandas as pd
import yaml
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

# -------------------------
# PATHS
# -------------------------
INPUT_DATA = "data/final/final_ranking_dataset.csv"
CONFIG_PATH = "config/ranking_weights.yaml"
OUTPUT_PATH = "outputs/material_rankings.csv"

Path("outputs").mkdir(exist_ok=True)

# -------------------------
# LOAD CONFIG
# -------------------------
with open(CONFIG_PATH, "r") as f:
    config = yaml.safe_load(f)

MODE = "balanced"  # change to sustainability / cost

weights = config["modes"][MODE]
constraints = config["constraints"]

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv(INPUT_DATA)

# Required columns check
required_cols = [
    "product_id",
    "Material Type",
    "predicted_cost",
    "predicted_co2",
    "Material Suitability Score",
    "Recyclability (%)",
    "Load Handling Score"
]

missing = set(required_cols) - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {missing}")

# -------------------------
# APPLY CONSTRAINTS
# -------------------------
df = df[
    (df["Recyclability (%)"] >= constraints["min_recyclability"]) &
    (df["Load Handling Score"] >= constraints["min_load_score"])
]

# -------------------------
# NORMALIZATION
# -------------------------
scaler = MinMaxScaler()

df[["cost_norm", "co2_norm", "suitability_norm"]] = scaler.fit_transform(
    df[[
        "predicted_cost",
        "predicted_co2",
        "Material Suitability Score"
    ]]
)

# -------------------------
# FINAL SCORE
# -------------------------
df["final_score"] = (
    weights["cost_weight"] * df["cost_norm"] +
    weights["co2_weight"] * df["co2_norm"] +
    weights["suitability_weight"] * (1 - df["suitability_norm"])
)

# -------------------------
# RANK PER PRODUCT
# -------------------------
df["rank"] = (
    df.groupby("product_id")["final_score"]
      .rank(method="dense", ascending=True)
)

# -------------------------
# SORT & SAVE
# -------------------------
df = df.sort_values(["product_id", "rank"])

df.to_csv(OUTPUT_PATH, index=False)

print("✅ Material ranking completed")
print(df.head())
