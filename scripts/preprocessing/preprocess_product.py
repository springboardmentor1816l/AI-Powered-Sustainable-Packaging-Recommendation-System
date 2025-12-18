import pandas as pd
from pathlib import Path

# Paths
RAW_PATH = Path("../../data/raw_datasets/product_dataset.csv")
OUT_PATH = Path("../../data/final/product_cleaned.parquet")
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

# Load
df = pd.read_csv(RAW_PATH)

# Standardize column names
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace("[^a-z0-9_]", "", regex=True)
)

# Separate types
num_cols = df.select_dtypes(include="number").columns
cat_cols = df.select_dtypes(include="object").columns

# Handle missing values
df[num_cols] = df[num_cols].fillna(df[num_cols].median())
df[cat_cols] = df[cat_cols].fillna("unknown")

# Save
df.to_parquet(OUT_PATH, index=False)
df.to_csv("../../data/processed/product_cleaned.csv",index=False)

print("product_cleaned.parquet created")
