import pandas as pd
import os

# Load combined engineered dataset
df = pd.read_csv(
    "data/combined(3)/combined_products_materials.csv"
)

# SELECT ONLY NUMERIC TARGETS (PDF REQUIRED)
y = df[[
    "cost_per_kg",
    "co2_emission_score"
]]

# Ensure folder exists
os.makedirs("data/model_ready(2)", exist_ok=True)

# Save targets
y.to_csv(
    "data/model_ready(2)/y_raw.csv",
    index=False
)

print("y_raw.csv created with cost and co2 targets")
