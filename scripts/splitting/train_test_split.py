import pandas as pd
import json
from pathlib import Path
from sklearn.model_selection import GroupShuffleSplit

# -----------------------------
# Paths
# -----------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
Y_PATH = Path("../../data/model_input/Y_raw.csv")
INTEGRATED_PATH = Path("../../data/integrated/integrated_dataset.csv")

OUT_DIR = Path("../../data/splits")
OUT_DIR.mkdir(parents=True, exist_ok=True)

META_DIR = Path("../../ml/metadata")
META_DIR.mkdir(parents=True, exist_ok=True)

RANDOM_SEED = 42
TEST_SIZE = 0.20
GROUP_COL = "product_id"  # in integrated dataset

# -----------------------------
# Load data
# -----------------------------
X = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)
integrated = pd.read_csv(INTEGRATED_PATH)

assert GROUP_COL in integrated.columns, f"Missing group column: {GROUP_COL}"

groups = integrated[GROUP_COL]

# Safety check
assert len(X) == len(groups), "X and group labels row mismatch"

# -----------------------------
# Group-aware split
# -----------------------------
gss = GroupShuffleSplit(
    n_splits=1,
    test_size=TEST_SIZE,
    random_state=RANDOM_SEED
)

train_idx, test_idx = next(gss.split(X, Y, groups=groups))

# -----------------------------
# Save indices
# -----------------------------
pd.Series(train_idx).to_csv(OUT_DIR / "train_indices.csv", index=False)
pd.Series(test_idx).to_csv(OUT_DIR / "test_indices.csv", index=False)

# -----------------------------
# Save metadata
# -----------------------------
split_metadata = {
    "dataset": {
        "features": "data/model_input/X_raw.csv",
        "targets": "data/model_input/Y_raw.csv",
        "integration_reference": "data/integrated/integrated_dataset.csv"
    },
    "split": {
        "method": "GroupShuffleSplit",
        "group_by": "product_product_id",
        "train_ratio": 0.8,
        "test_ratio": 0.2,
        "random_seed": 42
    },
    "cross_validation": {
        "method": "GroupKFold",
        "n_splits": 5,
        "group_by": "product_product_id"
    },
    "sizes": {
        "total_rows": int(len(X)),
        "train_rows": int(len(train_idx)),
        "test_rows": int(len(test_idx))
    },
    "design_notes": [
        "Identifiers excluded from model inputs",
        "Grouping applied via metadata only",
        "Leakage prevented at product level"
   ]
}

with open(META_DIR / "split_metadata.json", "w") as f:
    json.dump(split_metadata, f, indent=2)

print("Train/Test split created using product_id (without leaking into X)")
