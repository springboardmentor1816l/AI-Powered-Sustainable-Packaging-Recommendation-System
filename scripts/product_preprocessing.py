import pandas as pd
import os

RAW_PATH = "data/raw/product_dataset.csv"
OUTPUT_PATH = "data/processed/product_cleaned.csv"

os.makedirs("data/processed", exist_ok=True)

df = pd.read_csv(RAW_PATH)

print("Raw product data shape:", df.shape)
print("Columns:", df.columns.tolist())

# -----------------------------
# STANDARDIZE COLUMN NAMES
# -----------------------------
df.columns = df.columns.str.strip().str.lower()

# -----------------------------
# AUTO-DETECT WEIGHT COLUMN
# -----------------------------
weight_col = None
for col in df.columns:
    if "weight" in col:
        weight_col = col
        break

if weight_col is None:
    raise ValueError("❌ No weight column found in product dataset")

print("Detected weight column:", weight_col)

# -----------------------------
# BASIC CLEANING
# -----------------------------
df = df.drop_duplicates()

# -----------------------------
# HANDLE MISSING VALUES
# -----------------------------
if weight_col in df.columns:
    df[weight_col] = df[weight_col].fillna(df[weight_col].median())
    df = df[df[weight_col] > 0]

if "fragility_index" in df.columns:
    df["fragility_index"] = df["fragility_index"].fillna(df["fragility_index"].median())
    df["fragility_index"] = df["fragility_index"].astype(int).clip(1, 10)

# Categorical columns
for col in ["category", "shipping_type"]:
    if col in df.columns:
        df[col] = df[col].fillna("Unknown")

# -----------------------------
# RENAME WEIGHT COLUMN (STANDARD)
# -----------------------------
df = df.rename(columns={weight_col: "product_weight"})

# -----------------------------
# SAVE CLEANED DATA
# -----------------------------
df.to_csv(OUTPUT_PATH, index=False)

print("✅ Product preprocessing completed")
print("Saved at:", OUTPUT_PATH)
print("Final shape:", df.shape)
