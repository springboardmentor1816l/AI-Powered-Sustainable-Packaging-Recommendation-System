import joblib
import matplotlib.pyplot as plt
import pandas as pd
import os

# --------------------
# PATHS
# --------------------
MODEL_PATH = "ml/models/rf/rf_cost_v1.joblib"
PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
OUT_PATH = "outputs/explainability/feature_importance.png"

os.makedirs("outputs/explainability", exist_ok=True)

# --------------------
# LOAD MODEL & PIPELINE
# --------------------
print("Loading model and pipeline...")
model = joblib.load(MODEL_PATH)
pipeline = joblib.load(PIPELINE_PATH)

# --------------------
# GET FEATURE NAMES
# --------------------
num_features = pipeline.transformers_[0][2]
cat_features = pipeline.transformers_[1][1] \
    .named_steps["encoder"] \
    .get_feature_names_out(pipeline.transformers_[1][2])

feature_names = list(num_features) + list(cat_features)

# --------------------
# FEATURE IMPORTANCE
# --------------------
importances = model.feature_importances_

fi_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False).head(15)

# --------------------
# PLOT
# --------------------
plt.figure(figsize=(10, 6))
plt.barh(fi_df["feature"], fi_df["importance"])
plt.gca().invert_yaxis()
plt.title("Top Feature Importance – Cost Prediction Model")
plt.xlabel("Importance Score")
plt.tight_layout()

plt.savefig(OUT_PATH)
plt.close()

print(f"✅ Feature importance plot saved → {OUT_PATH}")
