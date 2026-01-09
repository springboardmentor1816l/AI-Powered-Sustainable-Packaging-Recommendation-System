import joblib
import pandas as pd


class MaterialSuitabilityPredictor:
    """
    Explainable, multi-factor suitability predictor.

    Factors used (Jan 5 compliance):
    - Cost efficiency
    - Strength adequacy
    - Recyclability
    - Biodegradability
    - CO₂ environmental impact
    - Fragility handling
    """

    # Centralized weights (easy to justify + tune)
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
        # Model kept for future ML extension (not blindly trusted)
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    # -----------------------------
    # Utility: Safe normalization
    # -----------------------------
    def _minmax(self, x, mn, mx):
        return max(0.0, min((x - mn) / (mx - mn + 1e-9), 1.0))

    # -----------------------------
    # Main prediction method
    # -----------------------------
    def predict(self, input_data, explain=False):

        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])

        # -----------------------------
        # Safe feature extraction
        # -----------------------------
        strength  = input_data.get("strength_mpa", pd.Series([50])).iloc[0]
        recycle   = input_data.get("recyclability_percent", pd.Series([50])).iloc[0]
        bio       = input_data.get("biodegradability_percent", pd.Series([50])).iloc[0]
        co2       = input_data.get("co2_emission_kg_per_kg", pd.Series([1.0])).iloc[0]
        fragility = input_data.get("fragility_index", pd.Series([3])).iloc[0]
        cost      = input_data.get("cost_per_kg", pd.Series([80])).iloc[0]

        fragility = max(1, min(int(fragility), 5))

        # -----------------------------
        # Normalized factor scores (0–1)
        # -----------------------------
        cost_score      = 1 - self._minmax(cost, 20, 200)
        strength_score  = self._minmax(strength, 5, 100)
        recycle_score   = self._minmax(recycle, 0, 100)
        bio_score       = self._minmax(bio, 0, 100)
        co2_score       = 1 - self._minmax(co2, 0.2, 5.0)
        fragility_score = 1 - ((fragility - 1) / 4)

        # -----------------------------
        # Final weighted suitability
        # -----------------------------
        suitability = (
            self.WEIGHTS["cost"] * cost_score +
            self.WEIGHTS["recyclability"] * recycle_score +
            self.WEIGHTS["strength"] * strength_score +
            self.WEIGHTS["biodegradability"] * bio_score +
            self.WEIGHTS["fragility"] * fragility_score +
            self.WEIGHTS["co2"] * co2_score
        )

        final_score = round(suitability * 100, 2)

        # -----------------------------
        # Explainability output
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

        # Backward-compatible return
        return [final_score]
