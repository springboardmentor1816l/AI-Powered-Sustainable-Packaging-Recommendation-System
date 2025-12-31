import pandas as pd
import yaml
import os

# Paths
PRED_PATH = "outputs/predicted_materials.csv"
CONFIG_PATH = "config/ranking_weights.yaml"
OUT_PATH = "outputs/material_rankings.csv"

# Load data
df = pd.read_csv(PRED_PATH)

# Load config
with open("config/ranking_weights.yaml") as f:
    config = yaml.safe_load(f)

weights = config["weights"]
constraints = config["constraints"]

print("Loaded constraints:", constraints)

# -----------------------------
# Apply constraints (filters)
# -----------------------------
df = df[
    (df["predicted_cost"] <= constraints["max_cost"]) &
    (df["recyclability"] >= constraints["min_recyclability"]) &
    (df["suitability_score"] >= constraints["min_suitability"])
]

# -----------------------------
# Normalize helper
# -----------------------------
def normalize(series, reverse=False):
    norm = (series - series.min()) / (series.max() - series.min() + 1e-9)
    return 1 - norm if reverse else norm

# -----------------------------
# Compute ranking score
# -----------------------------
df["cost_norm"] = normalize(df["predicted_cost"], reverse=True)
df["co2_norm"] = normalize(df["predicted_co2"], reverse=True)
df["suit_norm"] = normalize(df["suitability_score"])
df["sust_norm"] = normalize(df["sustainability_score"])

df["final_score"] = (
    weights["cost"] * df["cost_norm"] +
    weights["co2"] * df["co2_norm"] +
    weights["suitability"] * df["suit_norm"] +
    weights["sustainability"] * df["sust_norm"]
)

# -----------------------------
# Rank per product
# -----------------------------
df["rank"] = df.groupby("product_id")["final_score"] \
               .rank(ascending=False, method="dense")

df = df.sort_values(["product_id", "rank"])

# Save output
os.makedirs("outputs", exist_ok=True)
df.to_csv(OUT_PATH, index=False)

print("✅ Material ranking completed")
print(f"📄 Output saved to {OUT_PATH}")
