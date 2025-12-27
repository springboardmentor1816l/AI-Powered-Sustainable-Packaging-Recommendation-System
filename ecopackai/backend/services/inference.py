import pandas as pd
from services.model_loader import (
    rf_cost_model,
    xgb_co2_model,
    preprocessor
)

def _prepare_input(payload: dict):
    df = pd.DataFrame([payload])
    return preprocessor.transform(df)

def predict_cost(payload: dict) -> float:
    X = _prepare_input(payload)
    return float(rf_cost_model.predict(X)[0])

def predict_co2(payload: dict) -> float:
    X = _prepare_input(payload)
    return float(xgb_co2_model.predict(X)[0])
