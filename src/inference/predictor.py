from pathlib import Path
import joblib
import pandas as pd
from typing import Dict

BASE_DIR = Path(__file__).resolve().parents[2]  # project root

class EcoPackPredictor:
    def __init__(self):
        self.preprocessor = joblib.load(
            BASE_DIR / "models" / "preprocessing" / "preprocessing_pipeline.pkl"
        )
        self.cost_model = joblib.load(
            BASE_DIR / "ml" / "models" / "rf_cost.joblib"
        )
        self.co2_model = joblib.load(
            BASE_DIR / "ml" / "models" / "xgb_co2.joblib"
        )
        EXPECTED_FEATURES = list(self.preprocessor.feature_names_in_)


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
