# =========================================
# STEP 5: Permutation Feature Importance
# =========================================

import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from sklearn.inspection import permutation_importance

# -----------------------------------------
# Paths
# -----------------------------------------
MODEL_PATH = "models/trained/material_suitability_model.pkl"
PREPROCESSOR_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

X_TEST_PATH = "data/model_inputs/X_test.parquet"
Y_TEST_PATH = "data/model_inputs/y_test.parquet"

OUTPUT_DIR = "outputs/explainability"
OUTPUT_PATH = f"{OUTPUT_DIR}/feature_importance.png"

# -----------------------------------------
# Create output directory if not exists
# -----------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------------------
# Load model
# -----------------------------------------
model = joblib.load(MODEL_PATH)
print("✅ Model loaded")

# -----------------------------------------
# Load preprocessing pipeline
# -----------------------------------------
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("✅ Preprocessor loaded")

# -----------------------------------------
# Load test data
# -----------------------------------------
X_test = pd.read_parquet(X_TEST_PATH)
y_test = pd.read_parquet(Y_TEST_PATH)
print(f"✅ Test data loaded: {X_test.shape}")

# -----------------------------------------
# Apply preprocessing
# -----------------------------------------
X_test_processed = preprocessor.transform(X_test)
print("✅ Test data preprocessed")

# -----------------------------------------
# Compute permutation importance
# -----------------------------------------
result = permutation_importance(
    model,
    X_test_processed,
    y_test,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

print("✅ Permutation importance computed")

# -----------------------------------------
# Prepare feature importance ranking
# -----------------------------------------
feature_names = preprocessor.get_feature_names_out()
importances_mean = result.importances_mean

indices = np.argsort(importances_mean)[::-1]

# -----------------------------------------
# Plot top 10 important features
# -----------------------------------------
plt.figure(figsize=(10, 6))
plt.barh(
    [feature_names[i] for i in indices[:10]],
    importances_mean[indices[:10]]
)

plt.xlabel("Decrease in Model Performance")
plt.title("Permutation Feature Importance")
plt.gca().invert_yaxis()

plt.savefig(OUTPUT_PATH, bbox_inches="tight")
plt.close()

print(f"✅ Feature importance plot saved at: {OUTPUT_PATH}")
