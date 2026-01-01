import joblib
import pandas as pd
from pathlib import Path


class EcoPackPredictor:
    """
    Unified inference class for cost and CO2 prediction.
    Robust to legacy preprocessing / model feature mismatches.
    """

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[2]

        self.cost_model = joblib.load(
            self.base_dir / "ml" / "models" / "rf_cost.joblib"
        )
        self.co2_model = joblib.load(
            self.base_dir / "ml" / "models" / "xgb_co2.joblib"
        )
        self.preprocessor = joblib.load(
            self.base_dir / "preprocessing_pipeline.pkl"
        )

    def _prepare_input(self, X):
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        elif isinstance(X, list):
            X = pd.DataFrame(X)
        elif not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be DataFrame, dict, or list")

        # Enforce training feature columns
        if hasattr(self.preprocessor, "feature_names_in_"):
            X = X[list(self.preprocessor.feature_names_in_)]

        return self.preprocessor.transform(X)

    def predict(self, X):
        X_processed = self._prepare_input(X)

        # ---- COST (RandomForest expects 67) ----
        rf_n = self.cost_model.n_features_in_
        X_cost = X_processed[:, :rf_n]
        cost_pred = self.cost_model.predict(X_cost)

        # ---- CO2 (XGBoost expects 68) ----
        xgb_n = self.co2_model.get_booster().num_features()
        X_co2 = X_processed[:, :xgb_n]

        # 🔥 KEY FIX: disable feature re-validation
        co2_pred = self.co2_model.predict(
            X_co2,
            validate_features=False
        )

        return pd.DataFrame({
            "predicted_cost": cost_pred,
            "predicted_co2": co2_pred
        })
