import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =========================
# PATHS
# =========================
MODEL_PATH = "models/co2_impact_model.pkl"
DATASET_PATH = "data/integrated_with_co2_score.csv"
OUTPUT_DIR = "reports/shap"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# LOAD MODEL
# =========================
model = joblib.load(MODEL_PATH)
FEATURES = list(model.feature_names_in_)

print("✅ Model features:", FEATURES)

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATASET_PATH)

X = df[FEATURES].copy()

# Encode categoricals EXACTLY like training
for col in X.select_dtypes(include="object").columns:
    X[col] = X[col].astype("category").cat.codes

# Sample for speed
X_sample = X.sample(500, random_state=42)

# =========================
# SHAP (Multiclass-safe)
# =========================
explainer = shap.Explainer(model.predict_proba, X_sample)
shap_values = explainer(X_sample)

# Select HIGH CO₂ class (class index = 2)
shap_high = shap_values[:, :, 2]

# =========================
# BAR PLOT
# =========================
plt.figure()
shap.plots.bar(shap_high, show=False)
plt.title("SHAP Feature Importance – High CO₂ Impact")
plt.savefig(f"{OUTPUT_DIR}/co2_shap_bar.png", bbox_inches="tight", dpi=300)
plt.close()

# =========================
# SUMMARY PLOT
# =========================
plt.figure()
shap.plots.beeswarm(shap_high, show=False)
plt.title("SHAP Summary – High CO₂ Impact")
plt.savefig(f"{OUTPUT_DIR}/co2_shap_summary.png", bbox_inches="tight", dpi=300)
plt.close()

print("✅ CO₂ SHAP report generated successfully")
print(f"📊 Saved in: {OUTPUT_DIR}/")
