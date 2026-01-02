
import joblib
import pandas as pd

class EcoPackPredictor:
    def __init__(self, pipeline_path, cost_model_path, co2_model_path):
        self.pipeline = joblib.load(pipeline_path)
        self.cost_model = joblib.load(cost_model_path)
        self.co2_model = joblib.load(co2_model_path)

    def predict(self, df):
        X = self.pipeline.transform(df)
        cost = self.cost_model.predict(X)
        co2 = self.co2_model.predict(X)
        return {
            "predicted_cost": cost.tolist(),
            "predicted_co2": co2.tolist()
        }
