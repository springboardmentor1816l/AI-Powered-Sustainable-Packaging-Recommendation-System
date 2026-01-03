import pandas as pd
import joblib

# Paths
PIPELINE_PATH = "models/preprocessing/preprocessing_pipeline.pkl"
COST_MODEL_PATH = "ml/models/rf/rf_cost_v1.joblib"
CO2_MODEL_PATH = "ml/models/xgb/xgb_co2_v1.joblib"

# Load artifacts once
preprocessor = joblib.load(PIPELINE_PATH)
cost_model = joblib.load(COST_MODEL_PATH)
co2_model = joblib.load(CO2_MODEL_PATH)

def predict(input_df: pd.DataFrame):
    """
    input_df: integrated + engineered dataset (no target columns)
    returns: dataframe with predictions
    """
    X_transformed = preprocessor.transform(input_df)

    predicted_cost = cost_model.predict(X_transformed)
    predicted_co2 = co2_model.predict(X_transformed)

    result = input_df.copy()
    result["predicted_cost"] = predicted_cost
    result["predicted_co2"] = predicted_co2

    return result
