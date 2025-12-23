import pandas as pd
import numpy as np
import joblib
import os

from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
DATA_DIR = "data/model_ready"
X_train = pd.read_parquet(f"{DATA_DIR}/X_train.parquet")
X_test = pd.read_parquet(f"{DATA_DIR}/X_test.parquet")

y_train = pd.read_parquet(f"{DATA_DIR}/y_train.parquet")
y_test = pd.read_parquet(f"{DATA_DIR}/y_test.parquet")
y_train_numeric = y_train.select_dtypes(include=["int64", "float64"])
y_test_numeric = y_test.select_dtypes(include=["int64", "float64"])

print("Target columns used:", y_train_numeric.columns.tolist())

preprocessor = joblib.load(
    "models/preprocessing/preprocessing_pipeline.pkl"
)

X_train_transformed = preprocessor.transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

os.makedirs("ml/models", exist_ok=True)
os.makedirs("ml/metrics", exist_ok=True)

results = []
cost_model = LinearRegression()
cost_model.fit(
    X_train_transformed,
    y_train_numeric.iloc[:, 0]
)

cost_preds = cost_model.predict(X_test_transformed)

results.append({
    "model": "LinearRegression",
    "target": y_train_numeric.columns[0],
    "MAE": mean_absolute_error(y_test_numeric.iloc[:, 0], cost_preds),
    "RMSE": np.sqrt(mean_squared_error(y_test_numeric.iloc[:, 0], cost_preds)),
    "R2": r2_score(y_test_numeric.iloc[:, 0], cost_preds)
})

joblib.dump(
    cost_model,
    "ml/models/linear_regression_cost_v1.pkl"
)

co2_model = DecisionTreeRegressor(random_state=42)
co2_model.fit(
    X_train_transformed,
    y_train_numeric.iloc[:, 1]
)

co2_preds = co2_model.predict(X_test_transformed)

results.append({
    "model": "DecisionTreeRegressor",
    "target": y_train_numeric.columns[1],
    "MAE": mean_absolute_error(y_test_numeric.iloc[:, 1], co2_preds),
    "RMSE": np.sqrt(mean_squared_error(y_test_numeric.iloc[:, 1], co2_preds)),
    "R2": r2_score(y_test_numeric.iloc[:, 1], co2_preds)
})

joblib.dump(
    co2_model,
    "ml/models/decision_tree_co2_v1.pkl"
)

metrics_df = pd.DataFrame(results)
metrics_df.to_csv(
    "ml/metrics/baseline_metrics.csv",
    index=False
)

print("Baseline models trained and evaluated successfully")
