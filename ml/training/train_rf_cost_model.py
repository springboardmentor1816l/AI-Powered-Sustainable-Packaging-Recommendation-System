import pandas as pd
import numpy as np
import json
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# PATHS
# -----------------------------
X_PATH = "data/final/X_raw.csv"
Y_PATH = "data/final/Y_raw.csv"

PARAMS_PATH = "ml/experiments/exp_001/params.json"
METRICS_PATH = "ml/experiments/exp_001/metrics.json"

MODEL_DIR = "ml/models"
MODEL_NAME = "rf_cost_model_v1.pkl"
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# LOAD DATA
# -----------------------------
X = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)

y = Y["cost_per_kg"]

print("X shape:", X.shape)
print("y shape:", y.shape)

# -----------------------------
# HANDLE CATEGORICAL FEATURES
# (Simple encoding for RF)
# -----------------------------
X_encoded = pd.get_dummies(X, drop_first=True)

# -----------------------------
# LOAD PARAMS
# -----------------------------
with open(PARAMS_PATH, "r") as f:
    params = json.load(f)

rf_params = params["model_configuration"]

# -----------------------------
# TRAIN / TEST SPLIT
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y,
    test_size=params["train_test_split"]["test_ratio"],
    random_state=params["train_test_split"]["random_state"]
)

# -----------------------------
# MODEL TRAINING
# -----------------------------
model = RandomForestRegressor(
    n_estimators=rf_params["n_estimators"],
    max_depth=rf_params["max_depth"],
    min_samples_split=rf_params["min_samples_split"],
    min_samples_leaf=rf_params["min_samples_leaf"],
    max_features=rf_params["max_features"],
    bootstrap=rf_params["bootstrap"],
    random_state=rf_params["random_state"],
    n_jobs=rf_params["n_jobs"]
)

print("Training Random Forest model...")
model.fit(X_train, y_train)

# -----------------------------
# PREDICTION & EVALUATION
# -----------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("MAE:", mae)
print("RMSE:", rmse)
print("R2:", r2)

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(model, MODEL_PATH)

print("✅ Model saved at:", MODEL_PATH)

# -----------------------------
# SAVE METRICS
# -----------------------------
metrics = {
    "status": "trained",
    "mae": mae,
    "rmse": rmse,
    "r2_score": r2,
    "model_path": MODEL_PATH
}

with open(METRICS_PATH, "w") as f:
    json.dump(metrics, f, indent=2)

print("✅ Metrics saved at:", METRICS_PATH)
