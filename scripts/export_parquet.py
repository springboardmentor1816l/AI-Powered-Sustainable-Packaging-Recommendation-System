import pandas as pd
from pathlib import Path

df = pd.read_csv("cleaned_materials_ml_ready.csv")

Path("data/final").mkdir(parents=True, exist_ok=True)

df.to_parquet("data/final/materials_cleaned.parquet", index=False)
df.to_parquet("data/final/materials_engineered.parquet", index=False)
df.to_parquet("data/final/materials_model_ready.parquet", index=False)

print("Parquet files exported successfully")
