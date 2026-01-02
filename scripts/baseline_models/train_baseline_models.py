import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# -----------------------------
# Step 4.1: Load integrated data
# -----------------------------
X = pd.read_csv("data/model_inputs/integrated_X_raw.csv")
y = pd.read_csv("data/model_inputs/integrated_y_raw.csv")

print("X shape:", X.shape)
print("y shape:", y.shape)

# -----------------------------
# Step 4.2: Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Step 4.3: Train baseline model
# -----------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -----------------------------
# Step 4.4: Predict on test set
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Step 4.5: Compute metrics
# -----------------------------
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Baseline Model Evaluation")
print("-------------------------")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")

# -----------------------------
# Step 4.6: Save metrics
# -----------------------------
metrics_df = pd.DataFrame({
    "model": ["Linear Regression"],
    "MAE": [mae],
    "RMSE": [rmse],
    "R2": [r2]
})

os.makedirs("ml/metrics", exist_ok=True)
metrics_df.to_csv(
    "ml/metrics/baseline_metrics.csv",
    index=False
)

print("✅ Step 4 completed: Baseline metrics saved")
