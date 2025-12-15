import pandas as pd

df = pd.read_csv(
    "data/combined/combined_products_materials.csv"
)

df.to_parquet(
    "data/final/combined_model_ready.parquet",
    index=False
)

print("Final parquet saved")

