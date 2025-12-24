import joblib
import os

# -----------------------------
# MODEL VERSION INFO
# -----------------------------
MODEL_NAME = "material_recommendation"
MODEL_VERSION = "v1"

# -----------------------------
# OUTPUT PATH
# -----------------------------
MODEL_DIR = "ml/models"
MODEL_PATH = os.path.join(
    MODEL_DIR, f"{MODEL_NAME}_{MODEL_VERSION}.pkl"
)

os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# PLACEHOLDER MODEL OBJECT
# -----------------------------
dummy_model = {
    "model_name": MODEL_NAME,
    "version": MODEL_VERSION,
    "status": "not_trained",
    "notes": "Placeholder model artifact for versioning demonstration"
}

# -----------------------------
# SAVE MODEL
# -----------------------------
joblib.dump(dummy_model, MODEL_PATH)

print("✅ Model version saved successfully")
print("Model path:", MODEL_PATH)
