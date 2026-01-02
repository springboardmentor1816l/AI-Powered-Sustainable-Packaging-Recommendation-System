import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# Load data
# -----------------------------
X = pd.read_csv("data/model_inputs/integrated_X_raw.csv")
y = pd.read_csv("data/model_inputs/integrated_y_co2_raw.csv")

print("X shape:", X.shape)
print("y (CO2) shape:", y.shape)

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Train Decision Tree baseline
# -----------------------------
model = DecisionTreeRegressor(
    max_depth=5,
    random_state=42
)

model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Metrics
# -----------------------------
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("CO2 Baseline Model Evaluation")
print("-----------------------------")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

# -----------------------------
# Save / append metrics
# -----------------------------
metrics_row = pd.DataFrame({
    "model": ["Decision Tree"],
    "target": ["CO2_emission"],
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2]
})

os.makedirs("ml/metrics", exist_ok=True)

metrics_path = "ml/metrics/baseline_metrics.csv"

if os.path.exists(metrics_path):
    metrics_existing = pd.read_csv(metrics_path)
    metrics_final = pd.concat(
        [metrics_existing, metrics_row],
        ignore_index=True
    )
else:
    metrics_final = metrics_row

metrics_final.to_csv(metrics_path, index=False)

print("✅ Step 5B completed: CO2 baseline metrics added")
