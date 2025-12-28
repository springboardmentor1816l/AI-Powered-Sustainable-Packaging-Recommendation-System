import pandas as pd
import numpy as np
import joblib
import json
from pathlib import Path
from datetime import datetime

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# PATHS
# =========================
X_TRAIN = "data/splits/X_train.csv"
X_TEST = "data/splits/X_test.csv"
Y_TRAIN = "data/splits/y_train.csv"
Y_TEST = "data/splits/y_test.csv"

PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

MODEL_DIR = Path("ml/models/rf")
METRIC_DIR = Path("ml/metrics")
META_DIR = Path("ml/experiments/metadata")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)
META_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================
print("Loading datasets...")
X_train = pd.read_csv(X_TRAIN)
X_test = pd.read_csv(X_TEST)
y_train = pd.read_csv(Y_TRAIN)
y_test = pd.read_csv(Y_TEST)

# =========================
# LOAD PREPROCESSOR
# =========================
print("Loading preprocessing pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)

X_train_t = preprocessor.transform(X_train)
X_test_t = preprocessor.transform(X_test)

# =========================
# TARGET
# =========================
COST_TARGET = "Cost per Unit (USD)"

# =========================
# MODEL CONFIGURATION
# =========================
rf = RandomForestRegressor(
    n_estimators=200,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

# =========================
# TRAIN MODEL
# =========================
print("Training Random Forest model for cost prediction...")
rf.fit(X_train_t, y_train[COST_TARGET])

# =========================
# EVALUATION
# =========================
print("Evaluating model...")
y_pred = rf.predict(X_test_t)

mae = mean_absolute_error(y_test[COST_TARGET], y_pred)
rmse = np.sqrt(mean_squared_error(y_test[COST_TARGET], y_pred))
r2 = r2_score(y_test[COST_TARGET], y_pred)

metrics_df = pd.DataFrame([{
    "Model": "RandomForestRegressor",
    "Target": COST_TARGET,
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2
}])

metrics_df.to_csv(METRIC_DIR / "rf_cost_metrics.csv", index=False)

# =========================
# SAVE MODEL
# =========================
MODEL_PATH = MODEL_DIR / "rf_cost_v1.joblib"
joblib.dump(rf, MODEL_PATH)

# =========================
# SAVE METADATA
# =========================
metadata = {
    "experiment_id": "rf_cost_v1",
    "date": datetime.now().isoformat(),
    "model": "RandomForestRegressor",
    "hyperparameters": rf.get_params(),
    "dataset_version": "integrated_v1",
    "target": COST_TARGET,
    "metrics": {
        "MAE": mae,
        "RMSE": rmse,
        "R2": r2
    }
}

with open(META_DIR / "rf_cost_v1.json", "w") as f:
    json.dump(metadata, f, indent=4)

print("\n✅ Random Forest cost model trained successfully")
print(metrics_df)
