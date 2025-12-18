import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

IN_PATH = "data/interim/materials_cleaned.csv"
OUT_PATH = "data/final/materials_engineered.parquet"

print("🚀 Starting feature engineering")

df = pd.read_csv(IN_PATH)

# -----------------------------
# Raw Feature Calculations
# -----------------------------
df["CII_raw"] = (
    (1 / df["CO2 Emission per kg (estimated)"]) +
    (1 / df["Biodegradation Time (days)"])
)

df["CEI_raw"] = 1 / df["Cost per Unit (USD)"]

df["MSS_raw"] = (
    0.3 * df["moisture_resistance_score"] +
    0.3 * df["thermal_resistance_score"] +
    0.2 * df["Reusability (%)"] +
    0.2 * df["Waste Reduction Impact (%)"]
)

# -----------------------------
# Normalize Scores (0–100)
# -----------------------------
scaler = MinMaxScaler(feature_range=(0, 100))

df[["CII", "CEI", "MSS"]] = scaler.fit_transform(
    df[["CII_raw", "CEI_raw", "MSS_raw"]]
)

# -----------------------------
# Cleanup
# -----------------------------
df.drop(columns=["CII_raw", "CEI_raw", "MSS_raw"], inplace=True)

# Save
os.makedirs("data/final", exist_ok=True)
df.to_parquet(OUT_PATH, index=False)

print("✅ Feature engineered dataset saved to:", OUT_PATH)
