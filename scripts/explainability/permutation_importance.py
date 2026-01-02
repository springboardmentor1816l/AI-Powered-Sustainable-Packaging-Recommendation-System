import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.inspection import permutation_importance

# -------------------------------------------------
# Paths
# -------------------------------------------------
X_PATH = Path("../../data/model_input/X_raw.csv")
Y_PATH = Path("../../data/model_input/Y_raw.csv")
PREPROCESSOR_PATH = Path("../../models/preprocessing/preprocessing_pipeline.pkl")

RF_MODEL_PATH = Path("../../ml/models/rf_cost.joblib")
XGB_MODEL_PATH = Path("../../ml/models/xgb_co2.joblib")

OUT_DIR = Path("../../outputs/explainability")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------
# Load data
# -------------------------------------------------
X_raw = pd.read_csv(X_PATH)
Y = pd.read_csv(Y_PATH)

preprocessor = joblib.load(PREPROCESSOR_PATH)
X_proc = preprocessor.transform(X_raw)
feature_names = preprocessor.get_feature_names_out()

# -------------------------------------------------
# COST — Random Forest
# -------------------------------------------------
rf = joblib.load(RF_MODEL_PATH)
y_cost = Y["cost_per_unit_usd"]

rf_perm = permutation_importance(
    rf, X_proc, y_cost,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

rf_imp = pd.DataFrame({
    "feature": feature_names,
    "importance": rf_perm.importances_mean
}).sort_values("importance", ascending=False)

rf_imp.to_csv(OUT_DIR / "rf_cost_feature_importance.csv", index=False)

# Plot
plt.figure(figsize=(8, 6))
rf_imp.head(15).plot.barh(x="feature", y="importance")
plt.title("Permutation Importance — Cost (RF)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(OUT_DIR / "rf_cost_feature_importance.png", dpi=200)
plt.close()

# -------------------------------------------------
# CO2 — XGBoost
# -------------------------------------------------
xgb = joblib.load(XGB_MODEL_PATH)
y_co2 = Y["co2_emission_per_kg_estimated"]

xgb_perm = permutation_importance(
    xgb, X_proc, y_co2,
    n_repeats=10,
    random_state=42,
    n_jobs=-1
)

xgb_imp = pd.DataFrame({
    "feature": feature_names,
    "importance": xgb_perm.importances_mean
}).sort_values("importance", ascending=False)

xgb_imp.to_csv(OUT_DIR / "xgb_co2_feature_importance.csv", index=False)

plt.figure(figsize=(8, 6))
xgb_imp.head(15).plot.barh(x="feature", y="importance")
plt.title("Permutation Importance — CO₂ (XGBoost)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(OUT_DIR / "xgb_co2_feature_importance.png", dpi=200)
plt.close()

print("Permutation importance generated for RF and XGBoost")
