import pandas as pd
from pathlib import Path

INPUT = "data/interim/integrated_dataset.csv"

X_OUT = "data/final/X_regression_raw.csv"
Y_OUT = "data/final/y_regression_raw.csv"

FEATURES = [
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
]

TARGETS = [
    "cost_per_unit_usd",
    "co2_emission_per_kg_estimated",
]

df = pd.read_csv(INPUT)

X = df[FEATURES]
y = df[TARGETS]

Path("data/final").mkdir(parents=True, exist_ok=True)

# FORCE overwrite
X.to_csv(X_OUT, index=False)
y.to_csv(Y_OUT, index=False)

print("✅ Regression datasets recreated (FORCED)")
print("X shape:", X.shape)
print("y shape:", y.shape)
