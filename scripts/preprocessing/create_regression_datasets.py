import pandas as pd
import os

# ============================
# Paths
# ============================
IN_PATH = "data/interim/integrated_dataset.csv"

X_OUT = "data/final/X_regression_raw.csv"
Y_OUT = "data/final/y_regression_raw.csv"

os.makedirs("data/final", exist_ok=True)

# ============================
# Load integrated dataset
# ============================
df = pd.read_csv(IN_PATH)

print("Integrated dataset shape:", df.shape)

# ============================
# Targets (REGRESSION)
# ============================
TARGET_COLS = [
    "cost_per_unit_usd",
    "co2_emission_per_kg_estimated"
]

# ============================
# Features
# ============================
FEATURE_COLS = [
    "category",
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "material_type",
    "packaging_type",
    "recyclability_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "supplier_sustainability_compliance_pct",
    "sustainability_target_progress_pct"
]

# ============================
# Split X and y (SAME ROWS)
# ============================
X = df[FEATURE_COLS]
y = df[TARGET_COLS]

# ============================
# Save
# ============================
X.to_csv(X_OUT, index=False)
y.to_csv(Y_OUT, index=False)

print("✅ X_regression_raw shape:", X.shape)
print("✅ y_regression_raw shape:", y.shape)
