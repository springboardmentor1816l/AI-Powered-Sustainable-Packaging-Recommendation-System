"""
EcoPackAI – XGBoost CO₂ Emission Prediction Model
================================================
ERROR-FREE, MEMORY-SAFE, PRODUCTION-READY

Dataset:
- data/integrated_ecopack_dataset.csv

Outputs:
- ml/models/xgb_co2.joblib
- ml/metrics/co2_metrics.csv
"""

import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

# =========================
# Configuration
# =========================
DATA_PATH = "data/integrated_ecopack_dataset.csv"
MODEL_PATH = "ml/models/xgb_co2.joblib"
METRICS_PATH = "ml/metrics/co2_metrics.csv"

RANDOM_STATE = 42
TEST_SIZE = 0.2

os.makedirs("ml/models", exist_ok=True)
os.makedirs("ml/metrics", exist_ok=True)

# =========================
# Load Dataset
# =========================
print("📥 Loading integrated EcoPack dataset...")
df = pd.read_csv(DATA_PATH)

# =========================
# Target Variable
# =========================
TARGET_COL = "co2_impact_index"

if TARGET_COL not in df.columns:
    raise ValueError(f"Target column '{TARGET_COL}' not found in dataset")

y = df[TARGET_COL]

# =========================
# Feature Selection
# =========================
FEATURE_COLS = [
    "product_weight",
    "fragility_score",
    "moisture_sensitivity",
    "thermal_sensitivity",
    "expected_shelf_life_days",
    "material_cost_per_kg",
    "co2_emission_per_kg",
    "biodegradability_percent",
    "load_handling_score",
    "sustainability_score",
    "hazardous_material_flag",
    "product_category",
    "material_type",
    "recyclability_category",
    "supplier_region",
]

X = df[FEATURE_COLS].copy()

# =========================
# Encode Categorical Features (SAFE)
# =========================
categorical_cols = X.select_dtypes(include=["object"]).columns

label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    label_encoders[col] = le

# =========================
# Train-Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE
)

# =========================
# XGBoost Model (Memory Safe)
# =========================
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=120,
    max_depth=4,
    learning_rate=0.08,
    subsample=0.8,
    colsample_bytree=0.8,
    tree_method="hist",
    random_state=RANDOM_STATE,
    n_jobs=2
)

print("🚀 Training XGBoost CO₂ model...")
model.fit(X_train, y_train)

# =========================
# Evaluation
# =========================
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\n📊 Model Performance")
print(f"MAE : {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R²  : {r2:.4f}")

# =========================
# Save Metrics
# =========================
metrics_df = pd.DataFrame({
    "metric": ["MAE", "RMSE", "R2"],
    "value": [mae, rmse, r2]
})
metrics_df.to_csv(METRICS_PATH, index=False)

# =========================
# Save Model
# =========================
joblib.dump(model, MODEL_PATH)

print("\n✅ XGBoost CO₂ emission model training completed successfully")
print(f"📦 Model saved at: {MODEL_PATH}")
print(f"📈 Metrics saved at: {METRICS_PATH}")
