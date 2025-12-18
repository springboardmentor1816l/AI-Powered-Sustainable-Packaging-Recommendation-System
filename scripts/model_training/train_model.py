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
# Step 3: Transform data (THIS FIXES THE ERROR)
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

# -----------------------------
# Step 7: Save trained model
# -----------------------------
os.makedirs("models/trained", exist_ok=True)
joblib.dump(
    model,
    "models/trained/material_suitability_model.pkl"
)

print("✅ Model trained and saved successfully")
