import pandas as pd
import os

# -----------------------------
# Step 1: Load preprocessed data
# -----------------------------
products = pd.read_csv("data/preprocessed/products_preprocessed.csv")
materials = pd.read_csv("data/preprocessed/materials_preprocessed.csv")

print("Products shape:", products.shape)
print("Materials shape:", materials.shape)

# -----------------------------
# Step 2: Add temporary key
# -----------------------------
products["key"] = 1
materials["key"] = 1

# -----------------------------
# Step 3: Cartesian join (ALL combinations)
# -----------------------------
integrated_df = pd.merge(products, materials, on="key")

# Remove helper key
integrated_df.drop(columns=["key"], inplace=True)

print("Integrated dataset shape:", integrated_df.shape)

# -----------------------------
# Step 4: Save integrated dataset
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

integrated_df.to_csv(
    "data/processed/integrated_dataset.csv",
    index=False
)

print("✅ Step 1 completed: Integrated dataset saved")
