import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Union

class EcoPackPredictor:
    def __init__(self):
        self.preprocessor = joblib.load(
            Path("../../models/preprocessing/preprocessing_pipeline.pkl")
        )
        self.cost_model = joblib.load(
            Path("../../ml/models/rf_cost.joblib")
        )
        self.co2_model = joblib.load(
            Path("../../ml/models/xgb_co2.joblib")
        )

    def predict_batch(self, X_raw: pd.DataFrame) -> pd.DataFrame:
        X_proc = self.preprocessor.transform(X_raw)
        return pd.DataFrame({
            "predicted_cost": self.cost_model.predict(X_proc),
            "predicted_co2": self.co2_model.predict(X_proc)
        })

    def predict_one(self, record: Dict) -> Dict:
        df = pd.DataFrame([record])
        preds = self.predict_batch(df)
        return preds.iloc[0].to_dict()
