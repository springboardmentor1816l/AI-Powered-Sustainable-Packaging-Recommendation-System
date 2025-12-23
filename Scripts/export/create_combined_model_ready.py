import pandas as pd
import os

# Load feature matrix and targets
X = pd.read_csv("data/model_ready/X_raw.csv")
y = pd.read_csv("data/model_ready/y_raw.csv")

# Combine horizontally
combined = pd.concat([X, y], axis=1)

# Ensure folder exists
os.makedirs("data/model_ready", exist_ok=True)

# Save as parquet
combined.to_parquet(
    "data/model_ready/combined_model_ready.parquet",
    index=False
)

print("combined_model_ready.parquet created successfully")
