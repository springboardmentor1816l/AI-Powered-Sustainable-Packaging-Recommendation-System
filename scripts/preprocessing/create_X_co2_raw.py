import pandas as pd
from pathlib import Path

X = pd.read_csv("data/final/X_raw.csv")

TARGET_COLS = [
    "cost_per_unit_usd",
    "co2_emission_per_kg_estimated"
]

X_co2 = X.drop(columns=TARGET_COLS)

Path("data/final").mkdir(parents=True, exist_ok=True)
X_co2.to_csv("data/final/X_co2_raw.csv", index=False)

print("✅ X_co2_raw.csv created")
print(X_co2.columns.tolist())
