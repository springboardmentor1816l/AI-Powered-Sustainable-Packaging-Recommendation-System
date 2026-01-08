import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# Load integrated dataset
df = pd.read_csv("../data/processed/integrated_dataset.csv")

# ----------------------------
# Select features (X) and targets (Y)
# ----------------------------
X = df.drop(columns=["co2_score"])   # features
y_cost = df["recyclability"]          # target 1 (proxy for cost)
y_co2 = df["co2_score"]               # target 2

# Train-test split
X_train, X_test, y_cost_train, y_cost_test = train_test_split(
    X, y_cost, test_size=0.2, random_state=42
)

_, _, y_co2_train, y_co2_test = train_test_split(
    X, y_co2, test_size=0.2, random_state=42
)

# ----------------------------
# Model 1: Linear Regression (Cost)
# ----------------------------
lr = LinearRegression()
lr.fit(X_train, y_cost_train)
cost_pred = lr.predict(X_test)

# ----------------------------
# Model 2: Decision Tree (CO2)
# ----------------------------
dt = DecisionTreeRegressor(random_state=42)
dt.fit(X_train, y_co2_train)
co2_pred = dt.predict(X_test)

# ----------------------------
# Evaluation
# ----------------------------
metrics = []

def evaluate(y_true, y_pred, model, target):
    metrics.append({
        "model": model,
        "target": target,
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
        "R2": r2_score(y_true, y_pred)
    })

evaluate(y_cost_test, cost_pred, "Linear Regression", "Cost")
evaluate(y_co2_test, co2_pred, "Decision Tree", "CO2")

# Save metrics
metrics_df = pd.DataFrame(metrics)
metrics_df.to_csv("metrics/baseline_metrics.csv", index=False)

print("✅ Baseline models trained & metrics saved")

