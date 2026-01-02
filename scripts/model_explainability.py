import shap
import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

# =====================================================
# PATHS
# =====================================================
X_PATH = "data/final/X_raw.csv"
MODEL_PATH = "ml/models/rf_cost_model_v1.pkl"

OUTPUT_DIR = "outputs/explainability"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =====================================================
# LOAD DATA & MODEL
# =====================================================
X = pd.read_csv(X_PATH)

# Encode categorical features (same as training)
X_encoded = pd.get_dummies(X, drop_first=True)

model = joblib.load(MODEL_PATH)

# =====================================================
# SHAP EXPLAINER
# =====================================================
explainer = shap.TreeExplainer(model)

# Use sample for speed (IMPORTANT for large data)
X_sample = X_encoded.sample(1000, random_state=42)

shap_values = explainer.shap_values(X_sample)

# =====================================================
# SHAP SUMMARY PLOT
# =====================================================
plt.figure()
shap.summary_plot(
    shap_values,
    X_sample,
    show=False
)

SUMMARY_PATH = os.path.join(OUTPUT_DIR, "shap_summary.png")
plt.savefig(SUMMARY_PATH, bbox_inches="tight")
plt.close()

print("✅ SHAP summary plot saved at:", SUMMARY_PATH)

# =====================================================
# FEATURE IMPORTANCE (BAR)
# =====================================================
plt.figure()
shap.summary_plot(
    shap_values,
    X_sample,
    plot_type="bar",
    show=False
)

BAR_PATH = os.path.join(OUTPUT_DIR, "feature_importance.png")
plt.savefig(BAR_PATH, bbox_inches="tight")
plt.close()

print("✅ Feature importance plot saved at:", BAR_PATH)
