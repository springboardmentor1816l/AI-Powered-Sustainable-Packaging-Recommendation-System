import joblib
import pandas as pd


class MaterialSuitabilityPredictor:
    """
    Explainable, multi-factor material suitability predictor.

    Design principles:
    - Deterministic and explainable scoring
    - One-material-in → one-score-out
    - Ranking handled at API layer (correct separation of concerns)
    """

    # Centralized weights (academically justifiable)
    WEIGHTS = {
        "cost": 0.25,
        "recyclability": 0.20,
        "strength": 0.15,
        "biodegradability": 0.15,
        "fragility": 0.15,
        "co2": 0.10
    }

    def __init__(
        self,
        model_path="models/trained/material_suitability_model.pkl",
        preprocessor_path="models/preprocessing/preprocessing_pipeline.pkl",
    ):
        # Model kept for future hybrid ML usage (not mandatory for scoring)
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    # -----------------------------
    # Utility: Safe Min-Max Normalize
    # -----------------------------
    def _minmax(self, x, mn, mx):
        if mx - mn == 0:
            return 0.0
        return max(0.0, min((x - mn) / (mx - mn), 1.0))

    # -----------------------------
    # Main Prediction Method
    # -----------------------------
    def predict(self, input_data, explain=False):

        # Ensure DataFrame input
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])

        # -----------------------------
        # Feature Extraction (Safe Defaults)
        # -----------------------------
        strength  = float(input_data.get("strength_mpa", 50).iloc[0])
        recycle   = float(input_data.get("recyclability_percent", 50).iloc[0])
        bio       = float(input_data.get("biodegradability_percent", 50).iloc[0])
        co2       = float(input_data.get("co2_emission_kg_per_kg", 1.0).iloc[0])
        fragility = int(input_data.get("fragility_index", 3).iloc[0])
        cost      = float(input_data.get("cost_per_kg", 80).iloc[0])

        fragility = max(1, min(fragility, 5))

        # -----------------------------
        # Normalized Scores (0–1)
        # -----------------------------
        cost_score      = 1.0 - self._minmax(cost, 20, 200)
        strength_score  = self._minmax(strength, 5, 100)
        recycle_score   = self._minmax(recycle, 0, 100)
        bio_score       = self._minmax(bio, 0, 100)
        co2_score       = 1.0 - self._minmax(co2, 0.2, 5.0)
        fragility_score = 1.0 - ((fragility - 1) / 4)

        # -----------------------------
        # Weighted Suitability Score
        # -----------------------------
        suitability = (
            self.WEIGHTS["cost"] * cost_score +
            self.WEIGHTS["recyclability"] * recycle_score +
            self.WEIGHTS["strength"] * strength_score +
            self.WEIGHTS["biodegradability"] * bio_score +
            self.WEIGHTS["fragility"] * fragility_score +
            self.WEIGHTS["co2"] * co2_score
        )

        final_score = round(max(0.0, min(suitability * 100, 100.0)), 2)

        # -----------------------------
        # Explainability (Optional)
        # -----------------------------
        if explain:
            return {
                "final_score": final_score,
                "explanation": {
                    "cost_efficiency": round(cost_score * 100, 2),
                    "strength_adequacy": round(strength_score * 100, 2),
                    "recyclability": round(recycle_score * 100, 2),
                    "biodegradability": round(bio_score * 100, 2),
                    "co2_impact": round(co2_score * 100, 2),
                    "fragility_handling": round(fragility_score * 100, 2)
                }
            }

        # -----------------------------
        # Backward-Compatible Return
        # -----------------------------
        return [final_score]
