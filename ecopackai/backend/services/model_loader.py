import os
import joblib

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

rf_sustainability_pipeline = joblib.load(
    os.path.join(MODEL_DIR, "rf_sustainability_pipeline.joblib")
)
