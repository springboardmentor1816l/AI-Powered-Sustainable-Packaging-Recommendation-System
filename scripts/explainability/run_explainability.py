import shap
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")
RF_MODEL_PATH = Path("../../ml/models/rf_cost.joblib")
XGB_MODEL_PATH = Path("../../ml/models/xgb_co2.joblib")

OUT_DIR = Path("../../outputs/explainability")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load
# -------------------------------------------------
X_raw = pd.read_csv(X_PATH)
preprocessor = joblib.load(PREPROCESSOR_PATH)

X_proc = preprocessor.transform(X_raw)
feature_names = preprocessor.get_feature_names_out()

# Sample for SHAP (auto, representative)
sample_idx = np.linspace(0, X_proc.shape[0] - 1, num=200, dtype=int)
X_sample = X_proc[sample_idx]

# -------------------------------------------------
# RF — Cost
# -------------------------------------------------
rf = joblib.load(RF_MODEL_PATH)
rf_explainer = shap.TreeExplainer(rf)
rf_shap = rf_explainer.shap_values(X_sample)

plt.figure()
shap.summary_plot(
    rf_shap, X_sample, feature_names=feature_names, show=False
)
plt.tight_layout()
plt.savefig(OUT_DIR / "rf_cost_shap_summary.png", dpi=200)
plt.close()

rf_imp = pd.DataFrame({
    "feature": feature_names,
    "importance": np.abs(rf_shap).mean(axis=0)
}).sort_values("importance", ascending=False)

rf_imp.to_csv(OUT_DIR / "rf_cost_feature_importance.csv", index=False)

# -------------------------------------------------
# XGB — CO2
# -------------------------------------------------
xgb = joblib.load(XGB_MODEL_PATH)
xgb_explainer = shap.TreeExplainer(xgb)
xgb_shap = xgb_explainer.shap_values(X_sample)

plt.figure()
shap.summary_plot(
    xgb_shap, X_sample, feature_names=feature_names, show=False
)
plt.tight_layout()
plt.savefig(OUT_DIR / "xgb_co2_shap_summary.png", dpi=200)
plt.close()

xgb_imp = pd.DataFrame({
    "feature": feature_names,
    "importance": np.abs(xgb_shap).mean(axis=0)
}).sort_values("importance", ascending=False)

xgb_imp.to_csv(OUT_DIR / "xgb_co2_feature_importance.csv", index=False)

print("Explainability artifacts generated")
