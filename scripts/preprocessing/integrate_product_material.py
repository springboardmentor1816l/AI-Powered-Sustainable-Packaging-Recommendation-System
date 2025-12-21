import pandas as pd
import os

# ============================
# Paths
# ============================
PRODUCT_PATH = "data/processed/product_cleaned.csv"
MATERIAL_PATH = "data/processed/material_cleaned.csv"
OUT_PATH = "data/interim/integrated_dataset.csv"

os.makedirs("data/interim", exist_ok=True)

# ============================
# Load datasets
# ============================
products = pd.read_csv(PRODUCT_PATH)
materials = pd.read_csv(MATERIAL_PATH)

print("Products:", products.shape)
print("Materials:", materials.shape)

# ============================
# SIMPLE COMPATIBILITY LOGIC
# (baseline – no ML yet)
# ============================
integrated_rows = []

for _, p in products.iterrows():
    for _, m in materials.iterrows():

        # Basic logical filters
        if p["product_weight_kg"] <= m["load_handling_score"]:
            if p["fragility_index"] <= m["moisture_resistance_score"]:

                row = {
                    # Product
                    "product_id": p["product_id"],
                    "category": p["category"],
                    "product_weight_kg": p["product_weight_kg"],
                    "fragility_index": p["fragility_index"],
                    "shipping_type": p["shipping_type"],

                    # Material
                    "material_type": m["material_type"],
                    "packaging_type": m["packaging_type"],
                    "recyclability_pct": m["recyclability_pct"],
                    "load_handling_score": m["load_handling_score"],
                    "moisture_resistance_score": m["moisture_resistance_score"],
                    "thermal_resistance_score": m["thermal_resistance_score"],
                    "supplier_sustainability_compliance_pct": m["supplier_sustainability_compliance_pct"],
                    "sustainability_target_progress_pct": m["sustainability_target_progress_pct"],

                    # Targets
                    "cost_per_unit_usd": m["cost_per_unit_usd"],
                    "co2_emission_per_kg_estimated": m["co2_emission_per_kg_estimated"],
                }

                integrated_rows.append(row)

# ============================
# Save
# ============================
integrated_df = pd.DataFrame(integrated_rows)
integrated_df.to_csv(OUT_PATH, index=False)

print("✅ Integrated dataset created")
print("Shape:", integrated_df.shape)
