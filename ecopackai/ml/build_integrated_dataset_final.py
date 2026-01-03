# =========================================================
# EcoPackAI – Build Final Integrated Dataset (PDF-ALIGNED)
# =========================================================

import pandas as pd
import numpy as np
import os

# =========================================================
# 1️⃣ LOAD CLEAN DATASETS
# =========================================================
products = pd.read_csv("data/products_clean.csv")
materials = pd.read_csv("data/materials_clean.csv")

print("✅ Products:", products.shape)
print("✅ Materials:", materials.shape)

# =========================================================
# 2️⃣ EXPAND MATERIAL SUITABLE CATEGORIES
# =========================================================
materials["suitable_product_categories"] = (
    materials["suitable_product_categories"]
    .fillna("")
    .str.split(",")
)

materials = materials.explode("suitable_product_categories")
materials["suitable_product_categories"] = (
    materials["suitable_product_categories"].str.strip()
)

# =========================================================
# 3️⃣ SEMANTIC JOIN (PRODUCT ↔ MATERIAL)
# =========================================================
df = products.merge(
    materials,
    left_on="category",
    right_on="suitable_product_categories",
    how="inner"
)

print("🔗 Integrated dataset shape:", df.shape)

# =========================================================
# 4️⃣ ENGINEER MATERIAL SUITABILITY SCORE (PDF: Dec 10)
# =========================================================
df["material_suitability_score"] = (
    0.4 * (100 - df["biodegradation_time_days"]) +
    0.35 * df["recycled_content_percent"] +
    0.25 * df["reusability_percent"]
)

# =========================================================
# 5️⃣ COMPUTE SUSTAINABILITY SCORE (DECISION LOGIC)
# =========================================================
df["sustainability_score_final"] = (
    0.35 * (100 - df["co2_emission_score"]) +
    0.25 * (100 - df["cost_per_unit"]) +
    0.25 * df["material_suitability_score"] +
    0.15 * df["supplier_sustainability_compliance_percent"]
)

# =========================================================
# 6️⃣ SELECT FINAL COLUMNS
# =========================================================
final_columns = [
    # Product info
    "product_id",
    "product_name",
    "category",
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "fragility_level",

    # Material info
    "material_id",
    "material_type",
    "packaging_type",
    "supplier_region",

    # Material properties
    "biodegradation_time_days",
    "recycled_content_percent",
    "reusability_percent",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",

    # ML targets
    "cost_per_unit",
    "co2_emission_score",

    # Decision features
    "material_suitability_score",
    "supplier_sustainability_compliance_percent",
    "sustainability_score_final"
]

df = df[final_columns]

# =========================================================
# 7️⃣ SAVE FINAL DATASET
# =========================================================
os.makedirs("data", exist_ok=True)
output_path = "data/integrated_dataset_final_pdf.csv"
df.to_csv(output_path, index=False)

print("\n💾 Final integrated dataset saved to:")
print(output_path)
print("📊 Final shape:", df.shape)
