import pandas as pd
from ml.common_preprocessing import preprocess_common

# -----------------------------
# 1. Load dataset
# -----------------------------
df = pd.read_csv("data/products_raw.csv")

# -----------------------------
# 2. Standardize column names
# -----------------------------
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

# -----------------------------
# 3. Apply common preprocessing
# -----------------------------
df = preprocess_common(df)

# -----------------------------
# 4. Feature Engineering
# -----------------------------

# Normalize product weight
df["normalized_product_weight"] = (
    df["product_weight_kg"] / (df["product_weight_kg"].max() + 1)
)

# Encode fragility into categories
df["fragility_level"] = pd.cut(
    df["fragility_index"],
    bins=[-1, 0.3, 0.6, 1.0],
    labels=["low", "medium", "high"]
)

# -----------------------------
# 5. Save processed dataset
# -----------------------------
df.to_csv("data/products_clean.csv", index=False)

print("✅ Products preprocessing completed successfully")
print("Final shape:", df.shape)

