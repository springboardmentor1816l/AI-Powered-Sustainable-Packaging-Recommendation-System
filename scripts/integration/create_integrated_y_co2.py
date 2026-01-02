import pandas as pd
import os

# -----------------------------
# Load filtered integrated data
# -----------------------------
df = pd.read_csv(
    "data/processed/integrated_dataset_filtered.csv"
)

print("Dataset shape:", df.shape)

# -----------------------------
# Define CO2 target
# -----------------------------
TARGET_COLUMN = "co2_emission_kg_per_kg"

y_co2 = df[TARGET_COLUMN]

print("CO2 target shape:", y_co2.shape)

# -----------------------------
# Save CO2 target
# -----------------------------
os.makedirs("data/model_inputs", exist_ok=True)

y_co2.to_csv(
    "data/model_inputs/integrated_y_co2_raw.csv",
    index=False
)

print("✅ Step 5A completed: CO2 target saved")
