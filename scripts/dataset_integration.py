import pandas as pd
import os

# -----------------------------
# PATHS
# -----------------------------
PRODUCT_PATH = "data/processed/product_cleaned.csv"
MATERIAL_PATH = "data/processed/material_cleaned.csv"
OUTPUT_PATH = "data/processed/integrated_dataset.csv"

os.makedirs("data/processed", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
products = pd.read_csv(PRODUCT_PATH)
materials = pd.read_csv(MATERIAL_PATH)

print("Products:", products.shape)
print("Materials:", materials.shape)

# -----------------------------
# STANDARDIZE COLUMN NAMES
# -----------------------------
products.columns = products.columns.str.strip().str.lower()
materials.columns = materials.columns.str.strip().str.lower()

# -----------------------------
# CARTESIAN JOIN (Product × Material)
# -----------------------------
products["key"] = 1
materials["key"] = 1

merged = products.merge(materials, on="key").drop(columns="key")

print("After cartesian join:", merged.shape)

# -----------------------------
# RULE-BASED FILTERING
# -----------------------------

# 1. Weight compatibility
merged = merged[
    merged["weight_capacity"] >= merged["product_weight"]
]

# 2. Fragility vs strength (simple rule)
merged = merged[
    merged["strength_mpa"] >= merged["fragility_index"]
]

print("After compatibility rules:", merged.shape)

# -----------------------------
# OPTIONAL: CATEGORY / USE CASE MATCH
# (Soft filter – keep rows even if not matching)
# -----------------------------
merged["category_match"] = merged.apply(
    lambda row: row["category"].lower() in row["indusrty_use_case"].lower(),
    axis=1
)

# -----------------------------
# SAVE INTEGRATED DATA
# -----------------------------
merged.to_csv(OUTPUT_PATH, index=False)

print("✅ Dataset integration completed")
print("Integrated dataset saved at:", OUTPUT_PATH)
print("Final shape:", merged.shape)
