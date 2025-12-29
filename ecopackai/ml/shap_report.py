# ============================================================
# EcoPackAI – SHAP Report (ANALYSIS ONLY)
# Does NOT retrain or modify the model
# ============================================================

import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt

# -----------------------------
# CONFIG
# -----------------------------
DATASET_PATH = "data/integrated_dataset_shap_clean.csv"
MODEL_PATH = "backend/models/xgboost_sustainability_final.joblib"
RANDOM_STATE = 42

np.random.seed(RANDOM_STATE)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(DATASET_PATH)

# Drop same features used during training
DROP_FEATURES = [
    "product_id",
    "fragility_level",
    "load_handling_score",
    "moisture_resistance_score",
    "thermal_resistance_score"
]

df = df.drop(columns=[c for c in DROP_FEATURES if c in df.columns])

# -----------------------------
# FEATURE ENGINEERING (SAME AS TRAINING)
# -----------------------------
# Numeric binning
conditions = [
    df["product_weight_kg"] <= 0.5,
    (df["product_weight_kg"] > 0.5) & (df["product_weight_kg"] <= 2.0),
    df["product_weight_kg"] > 2.0
]
choices = [0, 1, 2]
df["product_weight_bin"] = np.select(conditions, choices, default=1)
df.drop(columns=["product_weight_kg"], inplace=True)

# Encode categorical
from sklearn.preprocessing import LabelEncoder

categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    df[col] = LabelEncoder().fit_transform(df[col])

# -----------------------------
# SPLIT FEATURES / TARGET
# -----------------------------
TARGET = "sustainability_score"
X = df.drop(columns=[TARGET])
y = df[TARGET]

# -----------------------------
# LOAD TRAINED MODEL
# -----------------------------
model_bundle = joblib.load(MODEL_PATH)
model = model_bundle["model"]

# -----------------------------
# SHAP EXPLAINER
# -----------------------------
print("🔍 Computing SHAP values (this may take a moment)...")

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X.sample(2000, random_state=RANDOM_STATE))

# -----------------------------
# SHAP SUMMARY PLOT
# -----------------------------
shap.summary_plot(
    shap_values,
    X.sample(2000, random_state=RANDOM_STATE),
    show=False
)

plt.title("SHAP Summary Plot – EcoPackAI")
plt.tight_layout()
plt.show()

# -----------------------------
# SHAP FEATURE IMPORTANCE TABLE
# -----------------------------
shap_importance = np.abs(shap_values).mean(axis=0)

shap_df = pd.DataFrame({
    "feature": X.columns,
    "mean_abs_shap_value": shap_importance
}).sort_values(by="mean_abs_shap_value", ascending=False)

print("\n📊 Top 10 Important Features (SHAP):")
print(shap_df.head(10))

# Optional: save report
shap_df.to_csv("shap_feature_importance_report.csv", index=False)
print("\n✅ SHAP report saved as shap_feature_importance_report.csv")


