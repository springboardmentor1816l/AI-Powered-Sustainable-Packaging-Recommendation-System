import joblib
import os

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "..", "models")

rf_cost_model = joblib.load(os.path.join(MODEL_DIR, "rf_cost.joblib"))
xgb_co2_model = joblib.load(os.path.join(MODEL_DIR, "xgb_co2.joblib"))
preprocessor = joblib.load(os.path.join(MODEL_DIR, "preprocessing_pipeline.pkl"))
