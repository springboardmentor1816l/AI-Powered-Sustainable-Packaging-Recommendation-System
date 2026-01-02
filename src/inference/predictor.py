import joblib
import pandas as pd

class EcoPackPredictor:
    def __init__(self):
        self.cost_model = joblib.load("ml/models/rf_cost_model_v1.pkl")
        self.co2_model = joblib.load("ml/models/xgb_co2_model_v1.joblib")

    def preprocess(self, df):
        # Simple encoding (same logic as training)
        return pd.get_dummies(df, drop_first=True)

    def predict_cost(self, df):
        X = self.preprocess(df)
        return self.cost_model.predict(X)

    def predict_co2(self, df):
        X = self.preprocess(df.drop(columns=["material_type"]))
        return self.co2_model.predict(X)

    def predict(self, df):
        cost_preds = self.predict_cost(df)
        co2_preds = self.predict_co2(df)

        output = df.copy()
        output["predicted_cost"] = cost_preds
        output["predicted_co2"] = co2_preds

        return output
