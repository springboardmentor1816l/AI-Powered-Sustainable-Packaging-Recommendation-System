import pandas as pd
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------
RAW_PATH = Path("../../data/raw_datasets/integrated_materials_dataset.csv")
OUT_DIR = Path("../../data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

CSV_OUT = OUT_DIR / "material_cleaned.csv"
PARQUET_OUT = "../../data/final/materials_cleaned.parquet"

# -----------------------------
# Load raw data
# -----------------------------
df = pd.read_csv(RAW_PATH)

# -----------------------------
# Standardize column names
# -----------------------------
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace(" ", "_")
      .str.replace(r"[^a-z0-9_]", "", regex=True)
)

# -----------------------------
# Identify column types
# -----------------------------
numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

# -----------------------------
# Handle missing values
# -----------------------------
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
df[categorical_cols] = df[categorical_cols].fillna("unknown")

# -----------------------------
# Apply value constraints
# -----------------------------
# Percentages
pct_cols = [c for c in df.columns if "percent" in c or c.endswith("_pct")]
for col in pct_cols:
    df[col] = df[col].clip(0, 100)

# Scores (must be non-negative)
score_cols = [c for c in df.columns if "score" in c]
for col in score_cols:
    df[col] = df[col].clip(lower=0)

# Cost (must be > 0)
if "cost_per_unit_usd" in df.columns:
    df = df[df["cost_per_unit_usd"] > 0]

# -----------------------------
# Save cleaned outputs
# -----------------------------
df.to_csv(CSV_OUT, index=False)
df.to_parquet(PARQUET_OUT, index=False)

print("material_cleaned.csv and material_cleaned.parquet created")
