# ==============================
# STEP 3: SHAP Global Explainability
# ==============================

import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
import os
from sklearn.inspection import permutation_importance

# ------------------------------
# Paths
# ------------------------------
MODEL_PATH = "models/trained/material_suitability_model.pkl"
PREPROCESSOR_PATH = "models/preprocessing/preprocessing_pipeline.pkl"

X_TEST_PATH = "data/model_inputs/X_test.parquet"
Y_TEST_PATH = "data/model_inputs/y_test.parquet"

OUTPUT_DIR = "outputs/explainability"
OUTPUT_PATH = f"{OUTPUT_DIR}/shap_summary.png"

# ------------------------------
# Create output directory if not exists
# ------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------
# Load model
# ------------------------------
model = joblib.load(MODEL_PATH)
print("✅ Model loaded successfully")

# ------------------------------
# Load preprocessing pipeline
# ------------------------------
preprocessor = joblib.load(PREPROCESSOR_PATH)
print("✅ Preprocessing pipeline loaded")

# ------------------------------
# Load test data
# ------------------------------
X_test = pd.read_parquet(X_TEST_PATH)
y_test = pd.read_parquet(Y_TEST_PATH)
print(f"✅ Test data loaded: {X_test.shape}")

# ------------------------------
# Sample test data for SHAP
# ------------------------------
X_shap = X_test.sample(200, random_state=42)
X_shap_processed = preprocessor.transform(X_shap)
print("✅ SHAP sample prepared")

# ------------------------------
# Initialize SHAP explainer
# ------------------------------
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_shap_processed)
print("✅ SHAP values computed")

# ------------------------------
# Generate SHAP summary plot
# ------------------------------
plt.figure()
shap.summary_plot(
    shap_values,
    X_shap_processed,
    feature_names=preprocessor.get_feature_names_out(),
    show=False
)

plt.savefig(OUTPUT_PATH, bbox_inches="tight")
plt.close()

print(f"✅ SHAP summary plot saved at: {OUTPUT_PATH}")

# ------------------------------
# Select one sample for local explanation
# ------------------------------
sample_index = 0

X_single = X_shap_processed[sample_index]
# ------------------------------
# Local SHAP explanation
# ------------------------------
shap.force_plot(
    explainer.expected_value,
    shap_values[sample_index],
    X_single,
    feature_names=preprocessor.get_feature_names_out(),
    matplotlib=True
)
plt.savefig("outputs/explainability/local_shap_explanation.png", bbox_inches="tight")
plt.close()

print("✅ Local SHAP explanation saved")

