import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
INTEGRATED_PATH = Path("../../data/integrated/integrated_dataset.csv")

OUT_DIR = Path("../../data/model_input")
OUT_DIR.mkdir(parents=True, exist_ok=True)

X_OUT = OUT_DIR / "X_raw.csv"
Y_OUT = OUT_DIR / "Y_raw.csv"

# -------------------------------------------------
# Load integrated dataset
# -------------------------------------------------
df = pd.read_csv(INTEGRATED_PATH)

# -------------------------------------------------
# Define target columns (Y)
# -------------------------------------------------
TARGET_COLS = [
    "cost_per_unit_usd",
    "co2_emission_per_kg_estimated"
]

# -------------------------------------------------
# Define columns to exclude from X
# -------------------------------------------------
ID_COLS = [
    "product_id",
    "material_id"
]

EXCLUDE_FROM_X = TARGET_COLS + ID_COLS

# -------------------------------------------------
# Build X and Y
# -------------------------------------------------
X = df.drop(columns=[c for c in EXCLUDE_FROM_X if c in df.columns])
Y = df[TARGET_COLS].copy()

# -------------------------------------------------
# Sanity checks
# -------------------------------------------------
assert not X.isnull().any().any(), "Missing values in X_raw"
assert not Y.isnull().any().any(), "Missing values in Y_raw"

# -------------------------------------------------
# Save outputs
# -------------------------------------------------
X.to_csv(X_OUT, index=False)
Y.to_csv(Y_OUT, index=False)

print("X_raw.csv and Y_raw.csv created successfully")
print(f"X shape: {X.shape}")
print(f"Y shape: {Y.shape}")
