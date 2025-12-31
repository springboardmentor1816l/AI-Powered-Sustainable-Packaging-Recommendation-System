import pandas as pd
import os

os.makedirs("outputs", exist_ok=True)

df = pd.read_csv("data/raw/EcoPackAI_dataset.csv")

out = pd.DataFrame({
    "product_id": range(len(df)),
    "material_id": df["Material ID"],
    "predicted_cost": df["Cost per Unit (USD)"],
    "predicted_co2": df["Carbon Footprint (kg CO2/unit)"],
    "suitability_score": (
        df["Load Handling Score"]
        + df["Moisture Resistance Score"]
        + df["Thermal Resistance Score"]
    ) / 3,
    "sustainability_score": df["Sustainability Target Progress (%)"] / 100,
    "recyclability": df["Recyclability (%)"] / 100
})

out.to_csv("outputs/predicted_materials.csv", index=False)

print("✅ outputs/predicted_materials.csv created")
print(out.head())
