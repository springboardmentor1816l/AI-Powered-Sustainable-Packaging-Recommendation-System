import joblib
import pandas as pd

class Predictor:
    def __init__(self):
        self.pipeline = joblib.load("models/preprocessing_pipeline.joblib")
        self.cost_model = joblib.load("models/rf_cost.joblib")
        self.co2_model = joblib.load("models/co2_model.pkl")

    def predict(self, data):
        if isinstance(data, dict):
            data = pd.DataFrame([data])
        elif isinstance(data, list):
            data = pd.DataFrame(data)

        processed = self.pipeline.transform(data)

        return {
            "cost_prediction": self.cost_model.predict(processed).tolist(),
            "co2_prediction": self.co2_model.predict(processed).tolist()
        }

predictor = Predictor()
