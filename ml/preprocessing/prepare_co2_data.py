import pandas as pd
import os

RAW_PATH = "data/raw/EcoPackAI_dataset.csv"
FINAL_DIR = "data/final"

os.makedirs(FINAL_DIR, exist_ok=True)

# Load raw dataset
df = pd.read_csv(RAW_PATH)

# -----------------------
# Target (y): CO2 emission
# -----------------------
y = df["Carbon Footprint (kg CO2/unit)"]
y.name = "co2_emission"

# -----------------------
# Features (X)
# -----------------------
X = df.drop(columns=["Carbon Footprint (kg CO2/unit)"])

# Keep only numeric columns (XGBoost requirement)
X = X.select_dtypes(include=["int64", "float64"])

# Save outputs
X.to_csv(f"{FINAL_DIR}/X_raw.csv", index=False)
y.to_csv(f"{FINAL_DIR}/y_co2.csv", index=False)

print("✅ CO2 data preparation complete")
print("X shape:", X.shape)
print("y shape:", y.shape)
