import pandas as pd
import numpy as np
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from pathlib import Path

# -----------------------
# PATHS
# -----------------------
X_TRAIN_PATH = "data/splits/X_train.csv"
X_TEST_PATH = "data/splits/X_test.csv"
Y_TRAIN_PATH = "data/splits/y_train.csv"
Y_TEST_PATH = "data/splits/y_test.csv"

PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
OUT_METRICS = Path("ml/metrics/baseline_metrics.csv")

# -----------------------
# LOAD DATA
# -----------------------
print("Loading datasets...")
X_train = pd.read_csv(X_TRAIN_PATH)
X_test = pd.read_csv(X_TEST_PATH)
y_train = pd.read_csv(Y_TRAIN_PATH)
y_test = pd.read_csv(Y_TEST_PATH)

# -----------------------
# LOAD PREPROCESSING PIPELINE
# -----------------------
print("Loading preprocessing pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)

# -----------------------
# APPLY PREPROCESSING (THIS FIXES YOUR ERROR)
# -----------------------
print("Transforming features...")
X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# -----------------------
# TARGETS
# -----------------------
COST_TARGET = "Cost per Unit (USD)"
CO2_TARGET = "CO2 Emission per kg (estimated)"

results = []

# =======================
# 1️⃣ COST MODEL — Linear Regression
# =======================
print("\nTraining Linear Regression (Cost Prediction)...")

lr = LinearRegression()
lr.fit(X_train_transformed, y_train[COST_TARGET])

y_pred_cost = lr.predict(X_test_transformed)

mae = mean_absolute_error(y_test[COST_TARGET], y_pred_cost)
rmse = np.sqrt(mean_squared_error(y_test[COST_TARGET], y_pred_cost))
r2 = r2_score(y_test[COST_TARGET], y_pred_cost)

results.append([
    "Linear Regression",
    COST_TARGET,
    mae,
    rmse,
    r2
])

# =======================
# 2️⃣ CO₂ MODEL — Decision Tree
# =======================
print("\nTraining Decision Tree (CO₂ Prediction)...")

dt = DecisionTreeRegressor(
    max_depth=8,
    random_state=42
)

dt.fit(X_train_transformed, y_train[CO2_TARGET])

y_pred_co2 = dt.predict(X_test_transformed)

mae = mean_absolute_error(y_test[CO2_TARGET], y_pred_co2)
rmse = np.sqrt(mean_squared_error(y_test[CO2_TARGET], y_pred_co2))
r2 = r2_score(y_test[CO2_TARGET], y_pred_co2)

results.append([
    "Decision Tree",
    CO2_TARGET,
    mae,
    rmse,
    r2
])

# -----------------------
# SAVE METRICS
# -----------------------
OUT_METRICS.parent.mkdir(parents=True, exist_ok=True)

metrics_df = pd.DataFrame(
    results,
    columns=["Model", "Target", "MAE", "RMSE", "R2"]
)

metrics_df.to_csv(OUT_METRICS, index=False)

print("\nBaseline metrics saved successfully.")
print(metrics_df)
