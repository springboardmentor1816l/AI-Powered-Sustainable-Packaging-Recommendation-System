import pandas as pd
import os
combined_path = "data/combined/combined_products_materials.csv"
df = pd.read_csv(combined_path)
target_cols = [
    "cost_per_kg",
    "co2_emission_score"
]
y = df[target_cols]
X = df.drop(columns=target_cols)
os.makedirs("data/model_ready", exist_ok=True)

X.to_csv("data/model_ready/X_raw.csv", index=False)
y.to_csv("data/model_ready/y_raw.csv", index=False)

print("✅ X_raw.csv and y_raw.csv created successfully")
