import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from datetime import datetime

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# PATHS
# =========================
X_TRAIN = "data/splits/X_train.csv"
X_TEST = "data/splits/X_test.csv"
Y_TRAIN = "data/splits/y_train.csv"
Y_TEST = "data/splits/y_test.csv"

PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

MODEL_DIR = Path("ml/models/baseline")
METRIC_DIR = Path("ml/metrics")
META_DIR = Path("ml/experiments/metadata")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================
X_train = pd.read_csv(X_TRAIN)
X_test = pd.read_csv(X_TEST)
y_train = pd.read_csv(Y_TRAIN)
y_test = pd.read_csv(Y_TEST)

preprocessor = joblib.load(PIPELINE_PATH)

X_train_t = preprocessor.transform(X_train)
X_test_t = preprocessor.transform(X_test)

COST_TARGET = "Cost per Unit (USD)"
CO2_TARGET = "CO2 Emission per kg (estimated)"

results = []

# =========================
# 1️⃣ COST MODEL
# =========================
lr = LinearRegression()
lr.fit(X_train_t, y_train[COST_TARGET])

cost_preds = lr.predict(X_test_t)

results.append({
    "model": "LinearRegression",
    "target": COST_TARGET,
    "MAE": mean_absolute_error(y_test[COST_TARGET], cost_preds),
    "RMSE": np.sqrt(mean_squared_error(y_test[COST_TARGET], cost_preds)),
    "R2": r2_score(y_test[COST_TARGET], cost_preds)
})

joblib.dump(lr, MODEL_DIR / "linear_regression_cost_v1.pkl")

# =========================
# 2️⃣ CO₂ MODEL
# =========================
dt = DecisionTreeRegressor(max_depth=8, random_state=42)
dt.fit(X_train_t, y_train[CO2_TARGET])

co2_preds = dt.predict(X_test_t)

results.append({
    "model": "DecisionTree",
    "target": CO2_TARGET,
    "MAE": mean_absolute_error(y_test[CO2_TARGET], co2_preds),
    "RMSE": np.sqrt(mean_squared_error(y_test[CO2_TARGET], co2_preds)),
    "R2": r2_score(y_test[CO2_TARGET], co2_preds)
})

joblib.dump(dt, MODEL_DIR / "decision_tree_co2_v1.pkl")

# =========================
# SAVE METRICS
# =========================
metrics_df = pd.DataFrame(results)
metrics_df.to_csv(METRIC_DIR / "baseline_metrics.csv", index=False)

# =========================
# SAVE METADATA
# =========================
metadata = {
    "experiment": "baseline_v1",
    "date": datetime.now().isoformat(),
    "models": ["LinearRegression", "DecisionTree"],
    "dataset": "integrated_dataset_v1",
    "features": list(X_train.columns),
    "targets": [COST_TARGET, CO2_TARGET]
}

with open(META_DIR / "baseline_v1.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("\n✅ Baseline training completed successfully")
print(metrics_df)
