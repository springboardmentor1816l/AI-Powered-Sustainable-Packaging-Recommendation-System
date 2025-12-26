import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
Y_PATH = Path("../../data/model_input/Y_raw.csv")
PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")

MODEL_DIR = Path("../models")
METRIC_DIR = Path("../metrics")
REPORT_DIR = Path("../reports")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
X_raw = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)

y = Y["co2_emission_per_kg_estimated"]

preprocessor = joblib.load(PREPROCESSOR_PATH)

# -------------------------------------------------
# Train–Test Split (80/20)
# -------------------------------------------------
X_train_raw, X_test_raw, y_train, y_test = train_test_split(
    X_raw, y, test_size=0.2, random_state=42
)

# -------------------------------------------------
# Preprocess
# -------------------------------------------------
X_train = preprocessor.fit_transform(X_train_raw)
X_test = preprocessor.transform(X_test_raw)

# -------------------------------------------------
# Model
# -------------------------------------------------
xgb = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

# -------------------------------------------------
# Train
# -------------------------------------------------
xgb.fit(X_train, y_train)

# -------------------------------------------------
# Evaluate
# -------------------------------------------------
preds = xgb.predict(X_test)

mae = mean_absolute_error(y_test, preds)
rmse = mean_squared_error(y_test, preds, squared=False)
r2 = r2_score(y_test, preds)

metrics_df = pd.DataFrame([{
    "model": "XGBoost",
    "target": "co2",
    "mae": mae,
    "rmse": rmse,
    "r2": r2
}])

metrics_df.to_csv(METRIC_DIR / "co2_metrics.csv", index=False)

# -------------------------------------------------
# Feature importance
# -------------------------------------------------
importance = xgb.feature_importances_
feature_names = preprocessor.get_feature_names_out()

fi_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importance
}).sort_values("importance", ascending=False)

fi_df.to_csv(REPORT_DIR / "feature_importance.csv", index=False)

# -------------------------------------------------
# Save model
# -------------------------------------------------
joblib.dump(xgb, MODEL_DIR / "xgb_co2.joblib")

print("XGBoost CO₂ model trained")
print(metrics_df)
