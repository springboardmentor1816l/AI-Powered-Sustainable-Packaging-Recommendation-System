import pandas as pd
from pathlib import Path
from sklearn.model_selection import GroupKFold

X_PATH = Path("../../data/model_input/X_raw.csv")
INTEGRATED_PATH = Path("../../data/integrated/integrated_dataset.csv")

OUT_DIR = Path("../../data/splits")
OUT_DIR.mkdir(parents=True, exist_ok=True)

GROUP_COL = "product_id"
N_SPLITS = 5

X = pd.read_csv(X_PATH)
integrated = pd.read_csv(INTEGRATED_PATH)

groups = integrated[GROUP_COL]

assert len(X) == len(groups), "X and group labels row mismatch"

gkf = GroupKFold(n_splits=N_SPLITS)

for fold, (train_idx, val_idx) in enumerate(gkf.split(X, groups=groups)):
    pd.Series(train_idx).to_csv(OUT_DIR / f"cv_fold_{fold}_train_idx.csv", index=False)
    pd.Series(val_idx).to_csv(OUT_DIR / f"cv_fold_{fold}_val_idx.csv", index=False)

print("GroupKFold splits created using product_id")
