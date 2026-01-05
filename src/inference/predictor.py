# =========================================
# Predictor Module
# Unified inference interface
# =========================================

import joblib
import pandas as pd


class MaterialSuitabilityPredictor:
    """
    Unified predictor for material suitability / cost prediction.
    """

    def __init__(
        self,
        model_path: str = "models/trained/material_suitability_model.pkl",
        preprocessor_path: str = "models/preprocessing/preprocessing_pipeline.pkl",
    ):
        """
        Initialize predictor by loading model and preprocessing pipeline.
        """
        self.model = joblib.load(model_path)
        self.preprocessor = joblib.load(preprocessor_path)

    def predict(self, input_data):
        """
        Generate predictions for input data.

        Parameters:
        - input_data: pandas DataFrame or dict (single record)

        Returns:
        - predictions (numpy array)
        """

        # Convert single input dict to DataFrame
        if isinstance(input_data, dict):
            input_data = pd.DataFrame([input_data])

        if not isinstance(input_data, pd.DataFrame):
            raise ValueError("Input data must be a pandas DataFrame or dict")

        # Apply preprocessing
        processed_data = self.preprocessor.transform(input_data)

        # Predict
        predictions = self.model.predict(processed_data)

        return predictions
