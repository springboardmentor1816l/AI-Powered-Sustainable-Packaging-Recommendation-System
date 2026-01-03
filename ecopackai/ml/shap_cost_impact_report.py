# =========================================================
# EcoPackAI – SHAP Report for COST IMPACT MODEL (FINAL)
# =========================================================

import pandas as pd
import shap
import joblib
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# =========================================================
# LOAD DATA
# =========================================================
DATA_PATH = "data/integrated_with_cost_score.csv"
MODEL_PATH = "models/cost_impact_model.pkl"

df = pd.read_csv(DATA_PATH)
print("✅ Dataset loaded:", df.shape)

# =========================================================
# FEATURES USED IN FINAL MODEL (MUST MATCH TRAINING)
# =========================================================
FEATURES = [
    "category",
    "shipping_type",
    "material_type",
    "packaging_type",
    "supplier_region",
    "product_weight_kg",
    "fragility_index",
    "reusability_percent",
    "supplier_sustainability_compliance_percent"
]

X = df[FEATURES].copy()

# Encode categoricals EXACTLY like training
for col in X.select_dtypes(include="object").columns:
    X[col] = LabelEncoder().fit_transform(X[col].astype(str))

# =========================================================
# LOAD TRAINED MODEL
# =========================================================
model = joblib.load(MODEL_PATH)
print("✅ Cost impact model loaded")

# =========================================================
# SHAP EXPLAINER (TREE-BASED)
# =========================================================
print("🔍 Computing SHAP values...")

# Use a SAMPLE for speed & stability
X_sample = X.sample(2000, random_state=42)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)

# =========================================================
# SHAP SUMMARY PLOT (GLOBAL IMPORTANCE)
# =========================================================
shap.summary_plot(
    shap_values,
    X_sample,
    plot_type="bar",
    show=False
)

plt.title("SHAP Feature Importance – Cost Impact Model")
plt.tight_layout()
plt.savefig("ml/shap_cost_impact_bar.png", dpi=300)
plt.close()

print("✅ SHAP bar plot saved: ml/shap_cost_impact_bar.png")

# =========================================================
# DETAILED SHAP SUMMARY (DOT PLOT)
# =========================================================
shap.summary_plot(
    shap_values,
    X_sample,
    show=False
)

plt.title("SHAP Summary Plot – Cost Impact Model")
plt.tight_layout()
plt.savefig("ml/shap_cost_impact_summary.png", dpi=300)
plt.close()

print("✅ SHAP summary plot saved: ml/shap_cost_impact_summary.png")




