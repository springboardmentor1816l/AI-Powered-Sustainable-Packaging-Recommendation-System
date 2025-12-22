import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import os

# --------------------
# Paths
# --------------------
X_PATH = "data/final/X_regression_encoded_scaled.csv"
Y_PATH = "data/final/y_regression_raw.csv"

MODEL_OUT = "ml/models/rf_cost.joblib"
METRICS_OUT = "ml/metrics/rf_cost_metrics.csv"
DOC_DIR = "docs"

os.makedirs("ml/models", exist_ok=True)
os.makedirs("ml/metrics", exist_ok=True)
os.makedirs(DOC_DIR, exist_ok=True)

# --------------------
# Load Data
# --------------------
X = pd.read_csv(X_PATH)
y = pd.read_csv(Y_PATH)

TARGET = "cost_per_unit_usd"
y_cost = y[TARGET]

print("X shape:", X.shape)
print("y shape:", y_cost.shape)

# --------------------
# Train/Test Split
# --------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

# --------------------
# Model Configuration
# --------------------
rf = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    n_jobs=-1
)

# --------------------
# Cross-Validation
# --------------------
cv = KFold(n_splits=5, shuffle=True, random_state=42)
cv_mae = -cross_val_score(
    rf,
    X_train,
    y_train,
    scoring="neg_mean_absolute_error",
    cv=cv
).mean()

# --------------------
# Train Model
# --------------------
rf.fit(X_train, y_train)

# --------------------
# Evaluate on Test Set
# --------------------
y_pred = rf.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

# --------------------
# Save Model
# --------------------
joblib.dump(rf, MODEL_OUT)

# --------------------
# Save Metrics
# --------------------
metrics = pd.DataFrame([{
    "model": "RandomForestRegressor",
    "target": TARGET,
    "mae": mae,
    "rmse": rmse,
    "r2": r2,
    "cv_mae": cv_mae
}])

metrics.to_csv(METRICS_OUT, index=False)

print("✅ Random Forest cost model trained successfully")
print(metrics)
print("📁 Model saved to:", MODEL_OUT)
print("📊 Metrics saved to:", METRICS_OUT)
