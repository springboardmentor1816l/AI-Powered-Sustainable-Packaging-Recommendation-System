import joblib
import pandas as pd


class EcoPackPredictor:
    def __init__(self):
        self.cost_model = joblib.load("ml/models/rf_cost_model_v1.pkl")
        self.co2_model = joblib.load("ml/models/xgb_co2_model_v1.joblib")

        self.cost_features = joblib.load("ml/models/rf_cost_features.joblib")
        self.co2_features = joblib.load("ml/models/xgb_co2_features.joblib")

    # 👇 THIS IS A CLASS METHOD (NOT inside __init__)
    def _prepare(self, df, features):
        X = pd.get_dummies(df, drop_first=True)

        # force exact training feature space
        X = X.reindex(columns=features, fill_value=0)

        return X

    def predict(self, df):
        X_cost = self._prepare(df, self.cost_features)
        X_co2 = self._prepare(
            df.drop(columns=["material_type"], errors="ignore"),
            self.co2_features
        )

        df_out = df.copy()
        df_out["predicted_cost"] = self.cost_model.predict(X_cost)
        df_out["predicted_co2"] = self.co2_model.predict(X_co2)

        return df_out
