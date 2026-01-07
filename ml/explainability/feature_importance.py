import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

# =========================
# Paths (ACTUAL FILES)
# =========================
MODEL_PATH = "ml/models/rf_cost_model_v1.pkl"
FEATURES_PATH = "ml/models/rf_cost_features.joblib"

OUTPUT_DIR = "ml/explainability"
OUTPUT_CSV = f"{OUTPUT_DIR}/feature_importance_cost.csv"
OUTPUT_PNG = f"{OUTPUT_DIR}/feature_importance_cost.png"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# Load model & feature names
# =========================
model = joblib.load(MODEL_PATH)
feature_names = joblib.load(FEATURES_PATH)

# =========================
# Feature Importance
# =========================
importances = model.feature_importances_

importance_df = pd.DataFrame({
    "feature": feature_names,
    "importance": importances
}).sort_values(by="importance", ascending=False)

# Save CSV
importance_df.to_csv(OUTPUT_CSV, index=False)

# =========================
# Plot Top 10
# =========================
plt.figure(figsize=(10, 6))
plt.barh(
    importance_df["feature"].head(10)[::-1],
    importance_df["importance"].head(10)[::-1]
)
plt.title("Top 10 Feature Importances (RF Cost Model)")
plt.xlabel("Importance Score")
plt.tight_layout()
plt.savefig(OUTPUT_PNG)

print("✅ Feature importance generated successfully")
print(f"📄 CSV saved at → {OUTPUT_CSV}")
print(f"📊 Plot saved at → {OUTPUT_PNG}")
