# =========================================
# STEP 7: Final Model Evaluation
# =========================================

import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

# -----------------------------------------
# Paths
# -----------------------------------------
MODEL_PATH = "models/trained/material_suitability_model.pkl"
PREPROCESSOR_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

X_TEST_PATH = "data/model_inputs/X_test.parquet"
Y_TEST_PATH = "data/model_inputs/y_test.parquet"

# -----------------------------------------
# Load model and preprocessing
# -----------------------------------------
model = joblib.load(MODEL_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

print("✅ Model and preprocessor loaded")

# -----------------------------------------
# Load test data
# -----------------------------------------
X_test = pd.read_parquet(X_TEST_PATH)
y_test = pd.read_parquet(Y_TEST_PATH)

# -----------------------------------------
# Preprocess test data
# -----------------------------------------
X_test_processed = preprocessor.transform(X_test)

# -----------------------------------------
# Generate predictions
# -----------------------------------------
y_pred = model.predict(X_test_processed)

# -----------------------------------------
# Compute evaluation metrics
# -----------------------------------------
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("📊 Final Model Evaluation Metrics")
print(f"MAE  : {mae:.4f}")
print(f"RMSE : {rmse:.4f}")
print(f"R²   : {r2:.4f}")
