import pandas as pd
import numpy as np
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from xgboost import XGBRegressor

# ---------------------------
# Paths
# ---------------------------
DATA_PATH = "data/interim/integrated_dataset.csv"
PREPROCESSOR_PATH = "models/preprocessing/co2_preprocessing_pipeline.pkl"


MODEL_OUT = "ml/models/xgb_co2.joblib"
METRICS_OUT = "ml/metrics/co2_metrics.csv"
FEATURE_IMPORTANCE_OUT = "reports/feature_importance.csv"

# ---------------------------
# Config
# ---------------------------
RANDOM_SEED = 42
TEST_SIZE = 0.2
TARGET_COL = "co2_emission_per_kg_estimated"

# ---------------------------
# Load integrated dataset
# ---------------------------
df = pd.read_csv(DATA_PATH)

# ---------------------------
# Define features & target (SAME DF)
# ---------------------------
FEATURE_COLS = [
    "product_weight_kg",
    "fragility_index",
    "shipping_type",
    "category",
    "packaging_type",
    "recyclability_pct",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score",
    "supplier_sustainability_compliance_pct",
    "sustainability_target_progress_pct",
]

X_raw = df[FEATURE_COLS]
y = df[TARGET_COL]

print(f"X shape: {X_raw.shape}")
print(f"y shape: {y.shape}")

# ---------------------------
# Load preprocessing pipeline
# ---------------------------
preprocessor = joblib.load(PREPROCESSOR_PATH)

X_processed = preprocessor.transform(X_raw)

# ---------------------------
# Train / test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_processed,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_SEED
)

# ---------------------------
# Model
# ---------------------------
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=RANDOM_SEED,
    n_jobs=-1
)

# ---------------------------
# Train
# ---------------------------
model.fit(X_train, y_train)

# ---------------------------
# Evaluate
# ---------------------------
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

metrics_df = pd.DataFrame([{
    "model": "XGBoostRegressor",
    "target": TARGET_COL,
    "mae": mae,
    "rmse": rmse,
    "r2": r2
}])

# ---------------------------
# Save outputs
# ---------------------------
Path("ml/models").mkdir(parents=True, exist_ok=True)
Path("ml/metrics").mkdir(parents=True, exist_ok=True)
Path("reports").mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_OUT)
metrics_df.to_csv(METRICS_OUT, index=False)

# ---------------------------
# Feature importance
# ---------------------------
feature_names = preprocessor.get_feature_names_out()

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

importance_df.to_csv(FEATURE_IMPORTANCE_OUT, index=False)

# ---------------------------
# Logs
# ---------------------------
print("✅ XGBoost CO₂ model trained successfully")
print(metrics_df)
print(f"📁 Model saved to: {MODEL_OUT}")
print(f"📊 Metrics saved to: {METRICS_OUT}")
print(f"📈 Feature importance saved to: {FEATURE_IMPORTANCE_OUT}")
