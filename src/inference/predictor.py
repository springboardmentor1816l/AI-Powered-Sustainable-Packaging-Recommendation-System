import joblib
import numpy as np
import pandas as pd

PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
COST_MODEL_PATH = "ml/models/rf/rf_cost_v1.joblib"
CO2_MODEL_PATH = "ml/models/xgb/xgb_co2_v1.joblib"

print("Loading models & pipeline...")
preprocessor = joblib.load(PIPELINE_PATH)
cost_model = joblib.load(COST_MODEL_PATH)
co2_model = joblib.load(CO2_MODEL_PATH)

def predict(input_data: dict):
    df = pd.DataFrame([input_data])

    X_transformed = preprocessor.transform(df)

    cost_pred = cost_model.predict(X_transformed)[0]
    co2_pred = co2_model.predict(X_transformed)[0]

    return {
        "predicted_cost": round(float(cost_pred), 3),
        "predicted_co2": round(float(co2_pred), 3)
    }
