import pandas as pd
import os

# -----------------------------
# PATHS
# -----------------------------
INPUT_PATH = "data/processed/integrated_dataset.csv"
X_OUTPUT = "data/final/X_raw.csv"
Y_OUTPUT = "data/final/Y_raw.csv"

os.makedirs("data/final", exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(INPUT_PATH)

print("Integrated dataset shape:", df.shape)

# -----------------------------
# DEFINE FEATURES (X)
# -----------------------------
X_columns = [
    "product_weight",
    "fragility_index",
    "shipping_type",
    "category",
    "material_type",
    "strength_mpa",
    "weight_capacity",
    "recyclability_percent",
    "biodegradability_percent"
]

X_raw = df[X_columns]

# -----------------------------
# DEFINE TARGETS (Y)
# -----------------------------
Y_columns = [
    "cost_per_kg",
    "co2_emission_score",
    "category_match"
]

Y_raw = df[Y_columns]

# -----------------------------
# SAVE FILES
# -----------------------------
X_raw.to_csv(X_OUTPUT, index=False)
Y_raw.to_csv(Y_OUTPUT, index=False)

print("✅ X_raw created:", X_raw.shape)
print("✅ Y_raw created:", Y_raw.shape)
print("Files saved in data/final/")
