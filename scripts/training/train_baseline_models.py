import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
Y_PATH = Path("../../data/model_input/Y_raw.csv")
INTEGRATED_PATH = Path("../../data/integrated/integrated_dataset.csv")

PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")

MODEL_DIR = Path("../../ml/models")
METRIC_DIR = Path("../../ml/metrics")
MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
X_raw = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)
groups = pd.read_csv(INTEGRATED_PATH)["product_id"]

preprocessor = joblib.load(PREPROCESSOR_PATH)

# -------------------------------------------------
# Targets
# -------------------------------------------------
TARGETS = {
    "cost": "cost_per_unit_usd",
    "co2": "co2_emission_per_kg_estimated"
}

MODELS = {
    "cost": LinearRegression(),
    "co2": DecisionTreeRegressor(random_state=42)
}

# -------------------------------------------------
# CV setup
# -------------------------------------------------
gkf = GroupKFold(n_splits=5)

records = []

# -------------------------------------------------
# Training + Evaluation
# -------------------------------------------------
for target_name, target_col in TARGETS.items():

    y = Y[target_col]
    model = MODELS[target_name]

    fold_metrics = []

    for fold, (train_idx, val_idx) in enumerate(gkf.split(X_raw, y, groups)):

        X_train = preprocessor.fit_transform(X_raw.iloc[train_idx])
        X_val = preprocessor.transform(X_raw.iloc[val_idx])

        y_train = y.iloc[train_idx]
        y_val = y.iloc[val_idx]

        model.fit(X_train, y_train)
        preds = model.predict(X_val)

        mae = mean_absolute_error(y_val, preds)
        rmse = mean_squared_error(y_val, preds, squared=False)
        r2 = r2_score(y_val, preds)

        records.append({
            "target": target_name,
            "fold": fold,
            "mae": mae,
            "rmse": rmse,
            "r2": r2
        })

        fold_metrics.append((mae, rmse, r2))

    # Save final model (trained on full data)
    X_all = preprocessor.fit_transform(X_raw)
    model.fit(X_all, y)

    joblib.dump(
        model,
        MODEL_DIR / f"baseline_{target_name}_model.pkl"
    )

    # Averages
    avg_mae, avg_rmse, avg_r2 = np.mean(fold_metrics, axis=0)

    records.append({
        "target": target_name,
        "fold": "avg",
        "mae": avg_mae,
        "rmse": avg_rmse,
        "r2": avg_r2
    })

# -------------------------------------------------
# Save metrics
# -------------------------------------------------
metrics_df = pd.DataFrame(records)
metrics_df.to_csv(METRIC_DIR / "baseline_metrics.csv", index=False)

print("Baseline training & evaluation completed")
print(metrics_df)
