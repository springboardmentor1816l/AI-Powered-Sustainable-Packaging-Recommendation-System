import pandas as pd

df = pd.read_csv("data/integrated_dataset.csv")

FINAL_COLUMNS = [
    # Product
    "product_id",
    "category",
    "product_weight_kg",
    "fragility_index",
    "fragility_level",
    "shipping_type",

    # Material
    "material_id",
    "material_type",
    "packaging_type",
    "biodegradation_time_days",
    "reusability_percent",
    "recycled_content_percent",
    "supplier_region",
    "supplier_sustainability_compliance_percent",

    # Performance
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",

    # Target
    "sustainability_score"
]

final_df = df[FINAL_COLUMNS]

final_df.to_csv(
    "data/integrated_dataset_shap_clean.csv",
    index=False
)

print("✅ SHAP-aligned integrated dataset created")
print("Shape:", final_df.shape)
