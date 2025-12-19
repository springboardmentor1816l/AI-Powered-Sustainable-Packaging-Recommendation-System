import pandas as pd

df = pd.read_csv(
    "data/combined/combined_products_materials.csv"
)

report = (
    df.groupby("material_id")
    .agg(
        avg_cost_per_kg=("cost_per_kg", "mean"),
        avg_co2_emission=("co2_emission_score", "mean"),
        avg_CII=("CII", "mean"),
        avg_CEI=("CEI", "mean"),
        avg_MSS=("MSS", "mean"),
        material_usage_count=("product_id", "count")
    )
    .reset_index()
)

report.to_parquet(
    "data/final/sustainability_reporting.parquet",
    index=False
)

print("Sustainability report created")

