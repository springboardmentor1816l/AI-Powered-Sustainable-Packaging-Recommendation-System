import joblib
import pandas as pd
import matplotlib.pyplot as plt
import os

MODEL_PATH = "models/xgb_co2_model.pkl"
OUTPUT_DIR = "outputs/explainability"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load trained model
model = joblib.load(MODEL_PATH)

# Get feature importance values
importances = model.feature_importances_

# ✅ Get feature names FROM model (not manually)
feature_names = model.get_booster().feature_names

# Sanity check (important)
assert len(importances) == len(feature_names), "Feature length mismatch"

# Build importance dataframe
fi = pd.Series(importances, index=feature_names).sort_values(ascending=False)

# Plot
plt.figure(figsize=(10, 6))
fi.plot(kind="barh")
plt.title("CO2 Model Feature Importance")
plt.xlabel("Importance")
plt.tight_layout()

# Save output
plt.savefig(f"{OUTPUT_DIR}/feature_importance.png")
plt.close()

print("✅ CO2 model explainability generated successfully")
