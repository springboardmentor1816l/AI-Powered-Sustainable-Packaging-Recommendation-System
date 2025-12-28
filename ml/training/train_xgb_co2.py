import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from datetime import datetime

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# =========================
# PATHS
# =========================
X_TRAIN = "data/splits/X_train.csv"
X_TEST = "data/splits/X_test.csv"
Y_TRAIN = "data/splits/y_train.csv"
Y_TEST = "data/splits/y_test.csv"

PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

MODEL_DIR = Path("ml/models/xgb")
METRIC_DIR = Path("ml/metrics")
REPORT_DIR = Path("ml/reports")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================
print("Loading datasets...")
X_train = pd.read_csv(X_TRAIN)
X_test = pd.read_csv(X_TEST)
y_train = pd.read_csv(Y_TRAIN)
y_test = pd.read_csv(Y_TEST)

# =========================
# LOAD PREPROCESSING PIPELINE
# =========================
print("Loading preprocessing pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)

X_train_t = preprocessor.transform(X_train)
X_test_t = preprocessor.transform(X_test)

# =========================
# TARGET
# =========================
CO2_TARGET = "CO2 Emission per kg (estimated)"

# =========================
# MODEL CONFIGURATION
# =========================
xgb = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

# =========================
# TRAIN MODEL
# =========================
print("Training XGBoost model for CO₂ prediction...")
xgb.fit(X_train_t, y_train[CO2_TARGET])

# =========================
# EVALUATION
# =========================
print("Evaluating model...")
y_pred = xgb.predict(X_test_t)

mae = mean_absolute_error(y_test[CO2_TARGET], y_pred)
rmse = np.sqrt(mean_squared_error(y_test[CO2_TARGET], y_pred))
r2 = r2_score(y_test[CO2_TARGET], y_pred)

metrics_df = pd.DataFrame([{
    "Model": "XGBoost Regressor",
    "Target": CO2_TARGET,
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2
}])

metrics_df.to_csv(METRIC_DIR / "xgb_co2_metrics.csv", index=False)

# =========================
# FEATURE IMPORTANCE
# =========================
feature_importance = pd.DataFrame({
    "feature_index": range(len(xgb.feature_importances_)),
    "importance": xgb.feature_importances_
}).sort_values(by="importance", ascending=False)

feature_importance.to_csv(REPORT_DIR / "xgb_co2_feature_importance.csv", index=False)

# =========================
# SAVE MODEL
# =========================
MODEL_PATH = MODEL_DIR / "xgb_co2_v1.joblib"
joblib.dump(xgb, MODEL_PATH)

print("\n✅ XGBoost CO₂ model trained successfully")
print(metrics_df)
