import shap
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

# --------------------
# PATHS
# --------------------
MODEL_PATH = "ml/models/rf/rf_cost_v1.joblib"
PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
X_PATH = "data/model_inputs/X_raw.csv"
OUT_PATH = "outputs/explainability/shap_summary.png"

os.makedirs("outputs/explainability", exist_ok=True)

# --------------------
# LOAD DATA & MODEL
# --------------------
print("Loading model, pipeline, and data...")
model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)
X = pd.read_csv(X_PATH).sample(300, random_state=42)

# --------------------
# TRANSFORM DATA
# --------------------
X_transformed = pipeline.transform(X)

# --------------------
# SHAP EXPLAINER
# --------------------
explainer = shap.Explainer(model)
shap_values = explainer(X_transformed)

# --------------------
# PLOT
# --------------------
shap.summary_plot(
    shap_values,
    X_transformed,
    show=False
)

plt.savefig(OUT_PATH, bbox_inches="tight")
plt.close()

print(f"✅ SHAP summary plot saved → {OUT_PATH}")
