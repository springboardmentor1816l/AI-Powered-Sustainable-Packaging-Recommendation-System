import pandas as pd
from ml.common_preprocessing import preprocess_common

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("data/materials_raw.csv")

# -----------------------------
# 2. Standardize column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("(", "")
    .str.replace(")", "")
    .str.replace("%", "percent")
)

# -----------------------------
# 3. Apply common preprocessing
# -----------------------------
df = preprocess_common(df)

# -----------------------------
# 4. Rename columns to ML-friendly names
# -----------------------------
df = df.rename(columns={
    "recyclability_percent": "recyclability_percent",
    "co2_emission_per_kg_estimated": "co2_emission_score",
    "biodegradation_time_days": "biodegradation_time_days",
    "cost_per_unit_usd": "cost_per_unit",
    "load_handling_score": "load_handling_score",
    "total_material_weight_tons": "total_material_weight"
})

# -----------------------------
# 5. Feature Engineering
# -----------------------------

# Convert biodegradation time to score (lower time = better)
df["biodegradability_score"] = 1 / (df["biodegradation_time_days"] + 1)

# Sustainability score
df["sustainability_score"] = (
    0.4 * df["recyclability_percent"] +
    0.3 * df["biodegradability_score"] -
    0.3 * df["co2_emission_score"]
)

# Cost efficiency
df["cost_efficiency"] = df["total_material_weight"] / df["cost_per_unit"]

# -----------------------------
# 6. Save processed dataset
# -----------------------------
df.to_csv("data/materials_clean.csv", index=False)

print("✅ Materials preprocessing completed successfully")
print("Final shape:", df.shape)
