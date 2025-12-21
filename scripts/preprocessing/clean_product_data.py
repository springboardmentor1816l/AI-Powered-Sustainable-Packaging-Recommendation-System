import pandas as pd
import os

INPUT_PATH = "data/raw/product_dataset.csv"
OUTPUT_PATH = "data/processed/product_cleaned.csv"

print("🚀 Cleaning product dataset")

df = pd.read_csv(INPUT_PATH)

print("Initial shape:", df.shape)

# -------------------------
# Standardize column names
# -------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# -------------------------
# Validate data types
# -------------------------
df["product_weight_kg"] = pd.to_numeric(df["product_weight_kg"], errors="coerce")
df["fragility_index"] = pd.to_numeric(df["fragility_index"], errors="coerce")

# -------------------------
# Handle missing values
# -------------------------
numeric_cols = ["product_weight_kg", "fragility_index"]
categorical_cols = ["category", "shipping_type"]

df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
df[categorical_cols] = df[categorical_cols].fillna("Unknown")

# -------------------------
# Final checks
# -------------------------
assert df.isnull().sum().sum() == 0, "❌ Missing values still exist"

os.makedirs("data/processed", exist_ok=True)
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Product dataset cleaned successfully")
print("Final shape:", df.shape)
print("Saved to:", OUTPUT_PATH)
