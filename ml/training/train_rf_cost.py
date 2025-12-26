import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
Y_PATH = Path("../../data/model_input/Y_raw.csv")
INTEGRATED_PATH = Path("../../data/integrated/integrated_dataset.csv")
PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")

MODEL_DIR = Path("../models")
METRIC_DIR = Path("../metrics")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
X_raw = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)
groups = pd.read_csv(INTEGRATED_PATH)["product_id"]

preprocessor = joblib.load(PREPROCESSOR_PATH)

y = Y["cost_per_unit_usd"]

# -------------------------------------------------
# Model
# -------------------------------------------------
rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

# -------------------------------------------------
# Cross-validation
# -------------------------------------------------
gkf = GroupKFold(n_splits=5)

records = []
fold_metrics = []

for fold, (train_idx, val_idx) in enumerate(gkf.split(X_raw, y, groups)):

    X_train = preprocessor.fit_transform(X_raw.iloc[train_idx])
    X_val = preprocessor.transform(X_raw.iloc[val_idx])

    y_train = y.iloc[train_idx]
    y_val = y.iloc[val_idx]

    rf.fit(X_train, y_train)
    preds = rf.predict(X_val)

    mae = mean_absolute_error(y_val, preds)
    rmse = mean_squared_error(y_val, preds, squared=False)
    r2 = r2_score(y_val, preds)

    records.append({
        "model": "RandomForest",
        "target": "cost",
        "fold": fold,
        "mae": mae,
        "rmse": rmse,
        "r2": r2
    })

    fold_metrics.append((mae, rmse, r2))

# -------------------------------------------------
# Averages
# -------------------------------------------------
avg_mae, avg_rmse, avg_r2 = np.mean(fold_metrics, axis=0)

records.append({
    "model": "RandomForest",
    "target": "cost",
    "fold": "avg",
    "mae": avg_mae,
    "rmse": avg_rmse,
    "r2": avg_r2
})

metrics_df = pd.DataFrame(records)
metrics_df.to_csv(METRIC_DIR / "rf_cost_metrics.csv", index=False)

# -------------------------------------------------
# Train final model on full data
# -------------------------------------------------
X_all = preprocessor.fit_transform(X_raw)
rf.fit(X_all, y)

joblib.dump(rf, MODEL_DIR / "rf_cost.joblib")

print("Random Forest cost model trained")
print(metrics_df)
