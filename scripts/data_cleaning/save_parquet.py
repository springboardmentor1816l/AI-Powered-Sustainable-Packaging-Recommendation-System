import pandas as pd
import os

INPUT = "data/processed/cleaned_dataset.csv"
OUT_DIR = "data/final"
OUT = os.path.join(OUT_DIR, "materials_cleaned.parquet")

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT)
df.to_parquet(OUT, index=False)
print("Saved parquet:", OUT)
