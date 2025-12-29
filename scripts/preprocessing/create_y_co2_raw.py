import pandas as pd
from pathlib import Path

# Paths
INPUT_Y = "data/final/y_regression_raw.csv"
OUTPUT_Y = "data/final/y_co2_raw.csv"

# Load
df = pd.read_csv("data/final/y_regression_raw.csv")
df[["co2_emission_per_kg_estimated"]].to_csv(
    "data/final/y_co2_raw.csv", index=False
)

# Extract CO₂ target
y_co2 = df[["co2_emission_per_kg_estimated"]]

# Save
Path("data/final").mkdir(parents=True, exist_ok=True)
y_co2.to_csv(OUTPUT_Y, index=False)

print("✅ y_co2_raw.csv created")
print("Shape:", y_co2.shape)
print("✅ y_co2_raw.csv recreated")
