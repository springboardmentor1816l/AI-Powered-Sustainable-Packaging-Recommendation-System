import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
from pathlib import Path

# ---------------------------
# Paths
# ---------------------------
X_PATH = "data/final/X_regression_raw.csv"
PREPROCESSOR_PATH = "models/preprocessing/co2_preprocessing_pipeline.pkl"
MODEL_PATH = "ml/models/xgb_co2.joblib"

OUTPUT_DIR = "outputs/explainability"
SHAP_SUMMARY_PNG = f"{OUTPUT_DIR}/shap_summary.png"
FEATURE_IMPORTANCE_PNG = f"{OUTPUT_DIR}/feature_importance.png"

# ---------------------------
# Config
# ---------------------------
SAMPLE_SIZE = 10000   # IMPORTANT: keep small for SHAP
RANDOM_SEED = 42

# ---------------------------
# Create output directory
# ---------------------------
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

# ---------------------------
# Load data
# ---------------------------
X_raw = pd.read_csv(X_PATH)

# Sample data for SHAP (very important for speed)
X_sample = X_raw.sample(
    n=min(SAMPLE_SIZE, len(X_raw)),
    random_state=RANDOM_SEED
)

print(f"Using SHAP sample size: {X_sample.shape}")

# ---------------------------
# Load preprocessing + model
# ---------------------------
preprocessor = joblib.load(PREPROCESSOR_PATH)
model = joblib.load(MODEL_PATH)

# ---------------------------
# Preprocess data
# ---------------------------
X_processed = preprocessor.transform(X_sample)

feature_names = preprocessor.get_feature_names_out()

# ---------------------------
# SHAP Explainer
# ---------------------------
explainer = shap.Explainer(model, X_processed)
shap_values = explainer(X_processed)

# ---------------------------
# SHAP Summary Plot
# ---------------------------
plt.figure(figsize=(10, 6))
shap.summary_plot(
    shap_values,
    X_processed,
    feature_names=feature_names,
    show=False
)
plt.tight_layout()
plt.savefig(SHAP_SUMMARY_PNG, dpi=300)
plt.close()

# ---------------------------
# Feature Importance (Mean |SHAP|)
# ---------------------------
mean_abs_shap = np.abs(shap_values.values).mean(axis=0)

importance_df = pd.DataFrame({
    "feature": feature_names,
    "mean_abs_shap": mean_abs_shap
}).sort_values(by="mean_abs_shap", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.barh(
    importance_df["feature"].head(15)[::-1],
    importance_df["mean_abs_shap"].head(15)[::-1]
)
plt.xlabel("Mean |SHAP value|")
plt.title("Top Feature Importance (XGBoost CO₂ Model)")
plt.tight_layout()
plt.savefig(FEATURE_IMPORTANCE_PNG, dpi=300)
plt.close()

# ---------------------------
# Save importance table (optional but useful)
# ---------------------------
importance_df.to_csv(
    f"{OUTPUT_DIR}/feature_importance.csv",
    index=False
)

# ---------------------------
# Logs
# ---------------------------
print("✅ SHAP explainability completed")
print(f"📊 SHAP summary saved to: {SHAP_SUMMARY_PNG}")
print(f"📈 Feature importance saved to: {FEATURE_IMPORTANCE_PNG}")
