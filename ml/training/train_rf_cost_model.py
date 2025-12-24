import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import joblib

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = Path("data/integrated_ecopack_dataset.csv")
MODEL_PATH = Path("ml/models/rf_cost.joblib")
METRICS_PATH = Path("ml/metrics/rf_cost_metrics.csv")
DOCS_PATH = Path("docs/rf_cost_training_summary.md")

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
DOCS_PATH.parent.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Load Dataset
# -----------------------------
df = pd.read_csv(DATA_PATH)

# -----------------------------
# Target Engineering
# -----------------------------
df["cost_per_unit"] = df["material_cost_per_kg"] * df["product_weight"]

TARGET_COL = "cost_per_unit"

# -----------------------------
# Feature Selection
# -----------------------------
FEATURE_COLS = [
    "product_weight",
    "fragility_score",
    "moisture_sensitivity",
    "thermal_sensitivity",
    "expected_shelf_life_days",
    "biodegradability_percent",
    "load_handling_score",
    "co2_impact_index",
    "cost_efficiency_index",
    "sustainability_score",
    "hazardous_material_flag",
]

X = df[FEATURE_COLS]
y = df[TARGET_COL]

# -----------------------------
# Train-Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Model Configuration
# -----------------------------
rf_model = RandomForestRegressor(
    n_estimators=300,
    max_depth=12,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

# -----------------------------
# Cross Validation
# -----------------------------
cv_scores = cross_val_score(
    rf_model, X_train, y_train, cv=5, scoring="neg_mean_absolute_error"
)
cv_mae = -cv_scores.mean()

# -----------------------------
# Model Training
# -----------------------------
rf_model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = rf_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(rf_model, MODEL_PATH)

# -----------------------------
# Save Metrics
# -----------------------------
metrics_df = pd.DataFrame([{
    "MAE": mae,
    "RMSE": rmse,
    "R2": r2,
    "CV_MAE": cv_mae
}])

metrics_df.to_csv(METRICS_PATH, index=False)

# -----------------------------
# Training Summary Doc
# -----------------------------
DOCS_PATH.write_text(f"""
# Random Forest Cost Prediction Model – Training Summary

## Dataset
- Source: integrated_ecopack_dataset.csv
- Records: {len(df)}

## Target Variable
- cost_per_unit = material_cost_per_kg × product_weight
- Unit: INR per product unit

## Features Used
{FEATURE_COLS}

## Model
- RandomForestRegressor
- Trees: 300
- Max Depth: 12
- Min Samples Split: 5
- Min Samples Leaf: 2

## Cross Validation
- 5-Fold CV MAE: {cv_mae:.4f}

## Test Metrics
- MAE: {mae:.4f}
- RMSE: {rmse:.4f}
- R² Score: {r2:.4f}

## Output Artifacts
- Model: ml/models/rf_cost.joblib
- Metrics: ml/metrics/rf_cost_metrics.csv
""")

print("✅ Random Forest Cost Model Training Completed Successfully")
print(f"MAE: {mae:.4f}")
print(f"RMSE: {rmse:.4f}")
print(f"R2: {r2:.4f}")
