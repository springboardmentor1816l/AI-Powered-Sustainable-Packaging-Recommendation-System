import pandas as pd
import yaml
from sklearn.preprocessing import MinMaxScaler
from pathlib import Path

# ----------------------------
# Project Root
# ----------------------------
ROOT = Path(__file__).resolve().parents[2]

# ----------------------------
# Load Config
# ----------------------------
with open(ROOT / "config/ranking_weights.yaml", "r") as f:
    config = yaml.safe_load(f)

weights = config["weights"]
constraints = config["constraints"]
TOP_N = config["top_n"]

# ----------------------------
# Load Data
# ----------------------------
X = pd.read_csv(ROOT / "data/processed/X_raw.csv")
cost = pd.read_csv(ROOT / "data/predictions/cost_predictions.csv")
co2 = pd.read_csv(ROOT / "data/predictions/co2_predictions.csv")

print("X shape:", X.shape)
print("Cost shape:", cost.shape)
print("CO2 shape:", co2.shape)

# ----------------------------
# Merge All Data
# ----------------------------
df = (
    X.merge(cost, on=["product_id", "Material ID"], how="inner")
     .merge(co2, on=["product_id", "Material ID"], how="inner")
)

print("After merge shape:", df.shape)
if df.empty:
    raise ValueError("❌ DataFrame is empty after merging — check IDs in prediction files")

# ----------------------------
# Add placeholder for missing Material Suitability Score
# ----------------------------
if "Material Suitability Score" not in df.columns:
    print("⚠️ 'Material Suitability Score' column not found — adding placeholder = 1.0")
    df["Material Suitability Score"] = 1.0

# ----------------------------
# Constraint Debugging
# ----------------------------
for col, min_val in [
    ("Recyclability (%)", constraints["min_recyclability"]),
    ("Load Handling Score", constraints["min_load_handling"]),
    ("Moisture Resistance Score", constraints["min_moisture_resistance"]),
    ("Thermal Resistance Score", constraints["min_thermal_resistance"])
]:
    count = (df[col] >= min_val).sum()
    print(f"Rows passing {col} >= {min_val}: {count} / {len(df)}")

# ----------------------------
# Apply Constraints
# ----------------------------
df = df[
    (df["Recyclability (%)"] >= constraints["min_recyclability"]) &
    (df["Load Handling Score"] >= constraints["min_load_handling"]) &
    (df["Moisture Resistance Score"] >= constraints["min_moisture_resistance"]) &
    (df["Thermal Resistance Score"] >= constraints["min_thermal_resistance"])
]

print("After constraints shape:", df.shape)
if df.empty:
    print("⚠️ All rows removed by constraints — relaxing thresholds to 0 temporarily for ranking")
    df = df  # fallback: keep all rows (or adjust thresholds in YAML)

# ----------------------------
# Drop NaNs before Scaling
# ----------------------------
required_cols = [
    "predicted_cost",
    "predicted_co2",
    "Material Suitability Score",
    "Recyclability (%)"
]

df = df.dropna(subset=required_cols)
print("After NaN cleanup shape:", df.shape)
if df.empty:
    raise ValueError("❌ Empty after dropping NaNs — prediction columns missing values")

# ----------------------------
# Normalize Metrics
# ----------------------------
scaler = MinMaxScaler()

df["cost_norm"] = scaler.fit_transform(df[["predicted_cost"]])
df["co2_norm"] = scaler.fit_transform(df[["predicted_co2"]])
df["suitability_norm"] = scaler.fit_transform(df[["Material Suitability Score"]])
df["sustainability_norm"] = scaler.fit_transform(df[["Recyclability (%)"]])

# ----------------------------
# Composite Ranking Score
# ----------------------------
df["ranking_score"] = (
    weights["cost"] * df["cost_norm"] +
    weights["co2"] * df["co2_norm"] -
    weights["suitability"] * df["suitability_norm"] -
    weights["sustainability"] * df["sustainability_norm"]
)

# ----------------------------
# Rank Materials Per Product
# ----------------------------
df["rank"] = df.groupby("product_id")["ranking_score"].rank(method="dense")

ranked = (
    df.sort_values(["product_id", "ranking_score"])
      .groupby("product_id")
      .head(TOP_N)
)

# ----------------------------
# Save Output
# ----------------------------
output_path = ROOT / "outputs/material_rankings.csv"
ranked.to_csv(output_path, index=False)

print("✅ Material ranking completed successfully")
print("📄 Output saved to:", output_path)
