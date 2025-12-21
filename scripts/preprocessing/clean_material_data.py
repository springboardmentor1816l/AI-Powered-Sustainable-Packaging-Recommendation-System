import pandas as pd
import os

INPUT_PATH = "data/raw/EcoPackAI_dataset.csv"
OUTPUT_PATH = "data/processed/material_cleaned.csv"

print("🚀 Cleaning material dataset")

df = pd.read_csv(INPUT_PATH)
print("Initial shape:", df.shape)

# -------------------------
# Standardize column names
# -------------------------
df.columns = [
    c.strip()
     .lower()
     .replace(" ", "_")
     .replace("-", "_")
     .replace("/", "_")
     .replace("%", "pct")
     .replace("(", "")
     .replace(")", "")
    for c in df.columns
]

# -------------------------
# Define columns
# -------------------------
numeric_cols = [
    "recyclability_pct",
    "recycled_content_pct",
    "reusability_pct",
    "biodegradation_time_days",
    "end_of_life_disposal_pct",
    "carbon_footprint_kg_co2_unit",
    "co2_emission_per_kg_estimated",
    "waste_reduction_impact_pct",
    "sustainability_target_progress_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "cost_per_unit_usd",
    "annual_usage_units",
    "total_material_weight_tons",
    "supplier_sustainability_compliance_pct"
]

categorical_cols = [
    "material_type",
    "packaging_type",
    "recyclability_category",
    "supplier_region"
]

df = df[numeric_cols + categorical_cols]

# -------------------------
# Convert numeric columns
# -------------------------
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------
# Handle missing values
# -------------------------
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
df[categorical_cols] = df[categorical_cols].fillna("Unknown")

# -------------------------
# Validation rules
# -------------------------
assert (df[numeric_cols] < 0).sum().sum() == 0, "❌ Negative values detected"
assert df.isnull().sum().sum() == 0, "❌ Missing values still exist"

# -------------------------
# Save cleaned dataset
# -------------------------
os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Material dataset cleaned successfully")
print("Final shape:", df.shape)
print("Saved to:", OUTPUT_PATH)
