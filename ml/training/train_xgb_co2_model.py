import pandas as pd
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

# =====================================================
# PATHS
# =====================================================
X_PATH = "data/final/X_raw.csv"
MATERIAL_PATH = "data/processed/material_cleaned.csv"

MODEL_DIR = "ml/models"
METRICS_DIR = "ml/metrics"
REPORTS_DIR = "ml/reports"

MODEL_PATH = os.path.join(MODEL_DIR, "xgb_co2_model_v1.joblib")
METRICS_PATH = os.path.join(METRICS_DIR, "xgb_co2_metrics.csv")
FEATURE_IMPORTANCE_PATH = os.path.join(REPORTS_DIR, "xgb_co2_feature_importance.csv")

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# =====================================================
# LOAD DATA
# =====================================================
X = pd.read_csv(X_PATH)
materials = pd.read_csv(MATERIAL_PATH)

print("X shape:", X.shape)
print("Materials shape:", materials.shape)

# =====================================================
# CREATE CO2 TARGET (AGGREGATED BY MATERIAL)
# =====================================================
co2_map = (
    materials
    .groupby("material_type")["co2_emission_score"]
    .mean()
)

y = X["material_type"].map(co2_map)

if y.isnull().any():
    missing = X.loc[y.isnull(), "material_type"].unique()
    raise ValueError(f"❌ Missing CO₂ mapping for materials: {missing}")

print("✅ CO₂ target created using material-level mean mapping")

# =====================================================
# FEATURES (DROP MATERIAL TYPE FROM INPUT)
# =====================================================
X_features = X.drop(columns=["material_type"])

# =====================================================
# ENCODING FOR XGBOOST
# =====================================================
X_encoded = pd.get_dummies(X_features, drop_first=True)

print("Encoded X shape:", X_encoded.shape)

# =====================================================
# TRAIN / TEST SPLIT
# =====================================================
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded,
    y,
    test_size=0.2,
    random_state=42
)

# =====================================================
# XGBOOST MODEL
# =====================================================
model = XGBRegressor(
    objective="reg:squarederror",
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

print("🚀 Training XGBoost CO₂ model...")
model.fit(X_train, y_train)

# =====================================================
# EVALUATION
# =====================================================
y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"MAE  : {mae:.6f}")
print(f"RMSE : {rmse:.6f}")
print(f"R²   : {r2:.6f}")

# =====================================================
# SAVE MODEL
# =====================================================
joblib.dump(model, MODEL_PATH)
print("✅ Model saved at:", MODEL_PATH)

# =====================================================
# SAVE METRICS
# =====================================================
pd.DataFrame([{
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2
}]).to_csv(METRICS_PATH, index=False)

print("✅ Metrics saved at:", METRICS_PATH)

# =====================================================
# FEATURE IMPORTANCE
# =====================================================
importance_df = pd.DataFrame({
    "feature": X_encoded.columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

importance_df.to_csv(FEATURE_IMPORTANCE_PATH, index=False)
print("✅ Feature importance saved at:", FEATURE_IMPORTANCE_PATH)

print("\n🎉 XGBoost CO₂ Emission Model Training COMPLETED SUCCESSFULLY")
