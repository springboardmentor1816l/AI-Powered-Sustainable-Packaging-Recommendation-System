import pandas as pd
import joblib
import os

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# Step 1: Load train-test data
# -----------------------------
X_train = pd.read_parquet("data/model_inputs/X_train.parquet")
X_test  = pd.read_parquet("data/model_inputs/X_test.parquet")

y_train = pd.read_parquet("data/model_inputs/y_train.parquet").squeeze()
y_test  = pd.read_parquet("data/model_inputs/y_test.parquet").squeeze()

# -----------------------------
# Step 2: Load preprocessing pipeline
# -----------------------------
preprocessor = joblib.load(
    "models/preprocessing/preprocessing_pipeline.pkl"
)

# -----------------------------
# Step 3: Transform data
# -----------------------------
X_train_processed = preprocessor.transform(X_train)
X_test_processed  = preprocessor.transform(X_test)

# -----------------------------
# Step 4: Create model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# -----------------------------
# Step 5: Train model
# -----------------------------
model.fit(X_train_processed, y_train)

# -----------------------------
# Step 6: Predict & evaluate
# -----------------------------
y_pred = model.predict(X_test_processed)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation Results")
print("------------------------")
print(f"MSE: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# =====================================================
# Step 7: MODEL VERSIONING (DEC 18 TASK)
# =====================================================

MODEL_NAME = "material_suitability"
MODEL_VERSION = "v1"

model_dir = f"ml/models/{MODEL_NAME}/{MODEL_VERSION}"
os.makedirs(model_dir, exist_ok=True)

model_path = f"{model_dir}/model.pkl"
joblib.dump(model, model_path)

print(f"✅ Model version {MODEL_VERSION} saved at: {model_path}")

# =====================================================
# Step 8: EXPERIMENT TRACKING (DEC 18 TASK)
# =====================================================

from datetime import datetime

experiment_dir = "ml/experiments"
os.makedirs(experiment_dir, exist_ok=True)

experiment_log_path = f"{experiment_dir}/experiment_log.csv"

experiment_data = {
    "model_name": MODEL_NAME,
    "model_version": MODEL_VERSION,
    "mse": mse,
    "r2_score": r2,
    "n_estimators": model.n_estimators,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

experiment_df = pd.DataFrame([experiment_data])

# Append if file exists, else create new
if os.path.exists(experiment_log_path):
    experiment_df.to_csv(
        experiment_log_path,
        mode="a",
        header=False,
        index=False
    )
else:
    experiment_df.to_csv(
        experiment_log_path,
        index=False
    )

print("📊 Experiment metrics logged successfully")
