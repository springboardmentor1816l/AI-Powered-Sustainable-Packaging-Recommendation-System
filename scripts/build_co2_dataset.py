import pandas as pd

# Load raw dataset
df = pd.read_csv("data/raw/EcoPackAI_dataset.csv")

# Target
y = df["Carbon Footprint (kg CO2/unit)"]
y.name = "co2_emission"

# Drop target from features
X = df.drop(columns=["Carbon Footprint (kg CO2/unit)"])

# Save final datasets
X.to_csv("data/final/X_raw.csv", index=False)
y.to_csv("data/final/y_co2.csv", index=False)

print("✅ Dataset built successfully")
print("X shape:", X.shape)
print("y shape:", y.shape)
