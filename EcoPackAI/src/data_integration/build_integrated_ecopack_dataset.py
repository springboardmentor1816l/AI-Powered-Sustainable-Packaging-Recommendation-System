"""
EcoPackAI — Build Integrated Product × Material Dataset

Purpose:
- Create integrated dataset required for preprocessing pipeline
- Combine product attributes and material attributes
- Generate engineered features

Output:
- data/integrated_ecopack_dataset.csv
"""

import os
import pandas as pd
import numpy as np


# ------------------------------------------------------------------
# 1. Paths (Windows-safe)
# ------------------------------------------------------------------
BASE_DIR = r"C:\Users\Tanmay\AI-Powered-Sustainable-Packaging-Recommendation-System"

PRODUCT_DATA_PATH = os.path.join(BASE_DIR, "data", "product_dataset.csv")
MATERIAL_DATA_PATH = os.path.join(BASE_DIR, "data", "material_dataset.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "integrated_ecopack_dataset.csv")

os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)


# ------------------------------------------------------------------
# 2. Load Datasets
# ------------------------------------------------------------------
print("📥 Loading product and material datasets...")

products_df = pd.read_csv(PRODUCT_DATA_PATH)
materials_df = pd.read_csv(MATERIAL_DATA_PATH)

print(f"Products: {products_df.shape}")
print(f"Materials: {materials_df.shape}")


# ------------------------------------------------------------------
# 3. Normalize Product Columns
# ------------------------------------------------------------------
products_df = products_df.rename(columns={
    "category": "product_category",
    "fragility_index": "fragility_score"
})


# ------------------------------------------------------------------
# 4. Derive Product Features (Rule-based)
# ------------------------------------------------------------------
products_df["moisture_sensitivity"] = products_df["shipping_type"].map({
    "Cold Chain": 1,
    "Standard": 0,
    "Dry": 0
}).fillna(0)

products_df["thermal_sensitivity"] = products_df["shipping_type"].map({
    "Cold Chain": 1,
    "Temperature Controlled": 1,
    "Standard": 0
}).fillna(0)

products_df["expected_shelf_life_days"] = products_df["product_category"].map({
    "Food": 30,
    "Pharmaceutical": 180,
    "Electronics": 365,
    "Cosmetics": 180
}).fillna(90)


# ------------------------------------------------------------------
# 5. Normalize Material Columns (FROM YOUR SCHEMA)
# ------------------------------------------------------------------
materials_df = materials_df.rename(columns={
    "cost_per_kg": "material_cost_per_kg",
    "co2_emission_kg_per_kg": "co2_emission_per_kg",
    "weight_capacity_kg": "load_handling_score"
})


# ------------------------------------------------------------------
# 6. Derive Material Features
# ------------------------------------------------------------------

# Recyclability category from percentage
materials_df["recyclability_category"] = pd.cut(
    materials_df["recyclability_percent"],
    bins=[0, 30, 70, 100],
    labels=["Low", "Medium", "High"]
)

# Hazardous material flag (rule-based assumption)
materials_df["hazardous_material_flag"] = materials_df["source_type"].apply(
    lambda x: 1 if str(x).lower() in ["chemical", "synthetic"] else 0
)

# Supplier region (derived from industry use case)
materials_df["supplier_region"] = materials_df["industry_use_case"].fillna("Global")


# ------------------------------------------------------------------
# 7. Validate Required Columns
# ------------------------------------------------------------------
required_product_cols = [
    "product_id",
    "product_category",
    "product_weight",
    "fragility_score",
    "moisture_sensitivity",
    "thermal_sensitivity",
    "expected_shelf_life_days"
]

required_material_cols = [
    "material_id",
    "material_type",
    "material_cost_per_kg",
    "co2_emission_per_kg",
    "load_handling_score",
    "recyclability_category",
    "supplier_region",
    "hazardous_material_flag"
]

for col in required_product_cols:
    if col not in products_df.columns:
        raise ValueError(f"Missing column in products.csv: {col}")

for col in required_material_cols:
    if col not in materials_df.columns:
        raise ValueError(f"Missing column in materials.csv: {col}")


# ------------------------------------------------------------------
# 8. Cartesian Join (Product × Material)
# ------------------------------------------------------------------
print("🔗 Creating Product × Material combinations...")

products_df["join_key"] = 1
materials_df["join_key"] = 1

integrated_df = pd.merge(
    products_df,
    materials_df,
    on="join_key",
    how="inner"
).drop(columns=["join_key"])

print(f"Integrated dataset shape: {integrated_df.shape}")


# ------------------------------------------------------------------
# 9. Feature Engineering
# ------------------------------------------------------------------
print("🧠 Generating engineered features...")

integrated_df["co2_impact_index"] = (
    integrated_df["co2_emission_per_kg"] *
    integrated_df["product_weight"]
)

integrated_df["cost_efficiency_index"] = (
    integrated_df["material_cost_per_kg"] *
    integrated_df["product_weight"]
)

integrated_df["suitability_score"] = (
    (10 - integrated_df["fragility_score"]) *
    integrated_df["load_handling_score"]
)

integrated_df["cost_efficiency_category"] = pd.qcut(
    integrated_df["cost_efficiency_index"],
    q=3,
    labels=["Low", "Medium", "High"]
)

integrated_df["sustainability_score"] = (
    100
    - integrated_df["co2_impact_index"].rank(pct=True) * 50
    + integrated_df["biodegradability_percent"].rank(pct=True) * 30
)

integrated_df["sustainability_score"] = (
    integrated_df["sustainability_score"]
    .clip(0, 100)
    .round(2)
)


# ------------------------------------------------------------------
# 10. Target Variable (Initial Heuristic)
# ------------------------------------------------------------------
print("🎯 Assigning recommended material...")

integrated_df["recommended_material"] = integrated_df.groupby(
    "product_id"
)["sustainability_score"].transform(
    lambda x: x == x.max()
)

integrated_df["recommended_material"] = np.where(
    integrated_df["recommended_material"],
    integrated_df["material_type"],
    "Not_Recommended"
)


# ------------------------------------------------------------------
# 11. Cleanup & Save
# ------------------------------------------------------------------
columns_order = [
    "product_id",
    "product_name",
    "product_category",
    "material_id",
    "material_type",
    "product_weight",
    "fragility_score",
    "moisture_sensitivity",
    "thermal_sensitivity",
    "expected_shelf_life_days",
    "material_cost_per_kg",
    "co2_emission_per_kg",
    "biodegradability_percent",
    "load_handling_score",
    "recyclability_category",
    "supplier_region",
    "hazardous_material_flag",
    "co2_impact_index",
    "cost_efficiency_index",
    "sustainability_score",
    "cost_efficiency_category",
    "recommended_material"
]

integrated_df = integrated_df[columns_order]

integrated_df.to_csv(OUTPUT_PATH, index=False)

print(f"✅ Integrated dataset saved to: {OUTPUT_PATH}")
print("🚀 Ready for preprocessing pipeline")
