import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold
import json
from pathlib import Path

# -----------------------
# CONFIG
# -----------------------
DATA_PATH = "data/integrated/product_material_integrated.csv"
OUT_SPLIT_DIR = Path("data/splits")
META_PATH = Path("ml/metadata/split_metadata.json")

RANDOM_SEED = 42
TEST_SIZE = 0.2
N_SPLITS = 5

# Stratification column (important!)
STRATIFY_COL = "category"  # product category

# Target variables
TARGET_COLS = [
    "Cost per Unit (USD)",
    "CO2 Emission per kg (estimated)"
]

# Columns to always drop from features
DROP_COLS = [
    "Material ID",
    "product_id",
    "product_name"
]

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)

# -----------------------
# DEFINE X & Y
# -----------------------
y = df[TARGET_COLS]
X = df.drop(columns=TARGET_COLS + DROP_COLS)

print("X shape:", X.shape)
print("Y shape:", y.shape)

# -----------------------
# TRAIN / TEST SPLIT
# -----------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_SEED,
    stratify=df[STRATIFY_COL]
)

# -----------------------
# SAVE SPLITS
# -----------------------
OUT_SPLIT_DIR.mkdir(parents=True, exist_ok=True)

X_train.to_csv(OUT_SPLIT_DIR / "X_train.csv", index=False)
X_test.to_csv(OUT_SPLIT_DIR / "X_test.csv", index=False)
y_train.to_csv(OUT_SPLIT_DIR / "y_train.csv", index=False)
y_test.to_csv(OUT_SPLIT_DIR / "y_test.csv", index=False)

print("Train/Test splits saved.")

# -----------------------
# CROSS-VALIDATION STRATEGY
# -----------------------
cv = StratifiedKFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_SEED
)

# -----------------------
# METADATA
# -----------------------
metadata = {
    "dataset": DATA_PATH,
    "rows": len(df),
    "features_count": X.shape[1],
    "targets": TARGET_COLS,
    "test_size": TEST_SIZE,
    "train_size": 1 - TEST_SIZE,
    "random_seed": RANDOM_SEED,
    "stratify_column": STRATIFY_COL,
    "cross_validation": {
        "type": "StratifiedKFold",
        "n_splits": N_SPLITS,
        "shuffle": True,
        "random_seed": RANDOM_SEED
    }
}

META_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(META_PATH, "w") as f:
    json.dump(metadata, f, indent=4)

print("Split metadata saved.")

