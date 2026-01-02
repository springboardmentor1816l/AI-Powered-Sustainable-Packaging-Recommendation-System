import pandas as pd
import os

# -----------------------------
# Step 1: Load integrated dataset
# -----------------------------
df = pd.read_csv("data/processed/integrated_dataset.csv")


print("Initial integrated shape:", df.shape)

# -----------------------------
# Step 2: Rule 1 - Weight compatibility
# Product weight must be <= material capacity
# -----------------------------
df = df[
    df["product_weight_kg"] <= df["weight_capacity_kg"]
]

print("After weight compatibility:", df.shape)

# -----------------------------
# Step 3: Rule 2 - Fragility vs material strength
# If product is fragile, material must be strong
# -----------------------------

FRAGILITY_THRESHOLD = 7      # higher = more fragile
STRENGTH_THRESHOLD = 60      # MPa

df = df[
    (df["fragility_index"] < FRAGILITY_THRESHOLD) |
    (df["strength_mpa"] >= STRENGTH_THRESHOLD)
]

print("After fragility-strength rule:", df.shape)


# -----------------------------
# Step 4: Save filtered dataset
# -----------------------------
os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/processed/integrated_dataset_filtered.csv",
    index=False
)

print("✅ Step 2 completed: Compatibility rules applied")
