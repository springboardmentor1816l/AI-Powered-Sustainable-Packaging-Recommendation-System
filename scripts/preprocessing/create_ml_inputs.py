import pandas as pd
import os

INPUT_PATH = "data/interim/integrated_dataset.csv"
X_OUT = "data/final/X_raw.csv"
Y_OUT = "data/final/y_raw.csv"

print("🚀 Creating ML inputs (X_raw, y_raw)")

df = pd.read_csv(INPUT_PATH)
print("Integrated shape:", df.shape)

TARGET = "material_type"

# -------------------------
# Define feature columns
# -------------------------
feature_cols = [
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "category",
    "packaging_type",
    "recyclability_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "supplier_sustainability_compliance_pct",
    "sustainability_target_progress_pct",
    "cost_per_unit_usd",
    "co2_emission_per_kg_estimated",
]

X = df[feature_cols]
y = df[TARGET]

os.makedirs("data/final", exist_ok=True)

X.to_csv(X_OUT, index=False)
y.to_csv(Y_OUT, index=False)

print("✅ X_raw shape:", X.shape)
print("✅ y_raw shape:", y.shape)
print("Saved to:")
print(" -", X_OUT)
print(" -", Y_OUT)
