import pandas as pd
import numpy as np
import os

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor

# -----------------------------
# Load data
# -----------------------------
X = pd.read_csv("data/model_inputs/integrated_X_raw.csv")

y_cost = pd.read_csv(
    "data/model_inputs/integrated_y_raw.csv"
).values.ravel()

y_co2 = pd.read_csv(
    "data/model_inputs/integrated_y_co2_raw.csv"
).values.ravel()

# -----------------------------
# Define models
# -----------------------------
cost_model = LinearRegression()
co2_model = DecisionTreeRegressor(
    max_depth=5,
    random_state=42
)

# -----------------------------
# Cross-validation
# -----------------------------
cost_cv_r2 = cross_val_score(
    cost_model, X, y_cost,
    cv=5, scoring="r2"
)

co2_cv_r2 = cross_val_score(
    co2_model, X, y_co2,
    cv=5, scoring="r2"
)

# -----------------------------
# Prepare results
# -----------------------------
cv_results = pd.DataFrame({
    "model": ["Linear Regression", "Decision Tree"],
    "target": ["Cost", "CO2"],
    "CV_R2_mean": [
        cost_cv_r2.mean(),
        co2_cv_r2.mean()
    ],
    "CV_R2_std": [
        cost_cv_r2.std(),
        co2_cv_r2.std()
    ]
})

# -----------------------------
# Save / append results
# -----------------------------
metrics_path = "ml/metrics/baseline_metrics.csv"

if os.path.exists(metrics_path):
    existing = pd.read_csv(metrics_path)
    final = pd.concat([existing, cv_results], ignore_index=True)
else:
    final = cv_results

final.to_csv(metrics_path, index=False)

print("✅ Step 5C completed: Cross-validation metrics added")
