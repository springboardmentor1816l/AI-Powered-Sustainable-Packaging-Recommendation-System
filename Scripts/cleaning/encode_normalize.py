import pandas as pd
from sklearn.preprocessing import MinMaxScaler

materials = pd.read_csv("data/processed(1)/materials_updated.csv")

# Normalize numeric columns
num_cols = ["strength_mpa", "weight_capacity",
            "biodegradability_percent",
            "co2_emission_score",
            "recyclability_percent",
            "cost_per_kg"]

scaler = MinMaxScaler()
materials[num_cols] = scaler.fit_transform(materials[num_cols])

# One-hot encode material type
materials = pd.get_dummies(materials, columns=["material_type"])

materials.to_csv("data/model_ready(2)/materials_final_encoded.csv", index=False)
print("✔ Encoded & normalized data saved")
