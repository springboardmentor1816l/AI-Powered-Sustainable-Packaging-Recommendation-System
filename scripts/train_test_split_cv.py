import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold

# -----------------------------
# LOAD MODEL-READY DATASET
# -----------------------------
DATA_PATH = "data/model_ready/materials_preprocessed_pipeline.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded:", df.shape)

# -----------------------------
# TARGET & FEATURES
# -----------------------------
# NOTE:
# For now, we simulate target creation for pipeline readiness.
# Actual target (recommended_material) will be added in next module.

# Dummy target for split & CV demonstration
df["recommended_material"] = "Cardboard"

X = df.drop(columns=["recommended_material"])
y = df["recommended_material"]

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Train set:", X_train.shape)
print("Test set:", X_test.shape)

# -----------------------------
# CROSS-VALIDATION SETUP
# -----------------------------
skf = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

print("Stratified K-Fold CV ready (K=5)")

# Show fold sizes
for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train), start=1):
    print(
        f"Fold {fold}: "
        f"Train size={len(train_idx)}, "
        f"Validation size={len(val_idx)}"
    )
