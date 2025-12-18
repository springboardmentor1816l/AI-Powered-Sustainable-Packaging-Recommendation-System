import os
import pandas as pd

RAW_PATH = "data/raw/EcoPackAI_dataset.csv"
OUT_DIR = "data/interim"
OUT_PATH = os.path.join(OUT_DIR, "materials_standardized.csv")

# Load raw data
df = pd.read_csv(RAW_PATH)

# Rename columns to snake_case
df = df.rename(columns={
    "Material ID": "material_id",
    "Packaging Type": "packaging_type",
    "Material Type": "material_type",
    "Suitable Product Categories": "suitable_product_categories",
    "Cost per Kg": "cost_per_kg",
    "CO2 Emission per Kg": "co2_emission_per_kg",
    "Moisture Resistance Score": "moisture_resistance_score",
    "Thermal Resistance Score": "thermal_resistance_score",
    "Biodegradation Time (Days)": "biodegradation_days",
    "Material Weight (tons)": "material_weight_tons",
    "Supplier Sustainability Compliance (%)": "supplier_sustainability_compliance_pct"
})

# Ensure output directory exists
os.makedirs(OUT_DIR, exist_ok=True)

# Save standardized data
df.to_csv(OUT_PATH, index=False)

print("✅ Standardized dataset written to:", OUT_PATH)
