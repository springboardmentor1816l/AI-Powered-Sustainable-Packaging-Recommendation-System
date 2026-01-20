import pandas as pd
import numpy as np
import joblib
import pickle
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
import logging
import warnings

warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EcoPackPredictor:
    """
    Unified Prediction Interface for EcoPackAI
    
    Provides a single entry point for making predictions with trained models.
    Handles preprocessing, model loading, prediction, and result formatting.
    """
    
    def __init__(
        self,
        cost_model_path: str = "ml/models/rf_cost.joblib",
        co2_model_path: str = "ml/models/xgb_co2.joblib",
        metadata_path: Optional[str] = None
    ):
        """
        Initialize predictor
        
        Args:
            cost_model_path: Path to cost prediction model
            co2_model_path: Path to CO₂ prediction model
            metadata_path: Path to metadata JSON (optional)
        """
        self.cost_model_path = cost_model_path
        self.co2_model_path = co2_model_path
        self.metadata_path = metadata_path or "src/inference/metadata.json"
        
        # Models
        self.cost_model = None
        self.co2_model = None
        
        # Metadata
        self.metadata = None
        self.feature_schema = None
        
        # Load models and metadata
        self._load_models()
        self._load_metadata()
        
        logger.info("EcoPackPredictor initialized successfully")
    
    def _load_models(self):
        """Load trained models"""
        logger.info("Loading models...")
        
        try:
            # Load cost model
            if Path(self.cost_model_path).exists():
                self.cost_model = joblib.load(self.cost_model_path)
                logger.info(f"✓ Loaded cost model from {self.cost_model_path}")
            else:
                logger.warning(f"Cost model not found: {self.cost_model_path}")
            
            # Load CO₂ model
            if Path(self.co2_model_path).exists():
                self.co2_model = joblib.load(self.co2_model_path)
                logger.info(f"✓ Loaded CO₂ model from {self.co2_model_path}")
            else:
                logger.warning(f"CO₂ model not found: {self.co2_model_path}")
                
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            raise
    
    def _load_metadata(self):
        """Load model metadata"""
        if Path(self.metadata_path).exists():
            try:
                with open(self.metadata_path, 'r') as f:
                    self.metadata = json.load(f)
                
                self.feature_schema = self.metadata.get('feature_schema', {})
                logger.info(f"✓ Loaded metadata from {self.metadata_path}")
                
            except Exception as e:
                logger.warning(f"Could not load metadata: {e}")
        else:
            logger.warning(f"Metadata file not found: {self.metadata_path}")
            self._create_default_metadata()
    
    def _create_default_metadata(self):
        """Create default metadata"""
        self.metadata = {
            "version": "1.0.0",
            "models": {
                "cost": {
                    "type": "Random Forest",
                    "path": self.cost_model_path
                },
                "co2": {
                    "type": "XGBoost",
                    "path": self.co2_model_path
                }
            }
        }
        logger.info("Created default metadata")
    
    def preprocess_input(self, X: Union[pd.DataFrame, Dict, List[Dict]]) -> pd.DataFrame:
        """
        Preprocess input data for prediction
        
        Args:
            X: Input features (DataFrame, dict, or list of dicts)
            
        Returns:
            Preprocessed DataFrame
        """
        # Convert to DataFrame if needed
        if isinstance(X, dict):
            X = pd.DataFrame([X])
        elif isinstance(X, list):
            X = pd.DataFrame(X)
        elif not isinstance(X, pd.DataFrame):
            raise ValueError("Input must be DataFrame, dict, or list of dicts")
        
        # Add missing categorical features with defaults
        categorical_defaults = {
            'packaging_type': 'Cardboard Boxes',
            'suitable_product_categories': 'General',
            'recommended_packaging_use_cases': 'Standard',
            'supplier_region': 'EMEA',
            'recyclability_category': 'High'
        }
        
        for col, default_value in categorical_defaults.items():
            if col not in X.columns:
                X[col] = default_value
                logger.debug(f"Added missing categorical feature '{col}' with default '{default_value}'")
        
        # Validate required features
        if self.feature_schema:
            required_features = self.feature_schema.get('required_features', [])
            missing_features = set(required_features) - set(X.columns)
            
            if missing_features:
                logger.warning(f"Missing features: {missing_features}")
        
        return X
    
    def predict_cost(
        self,
        X: Union[pd.DataFrame, Dict, List[Dict]],
        return_confidence: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Predict cost per unit
        
        Args:
            X: Input features
            return_confidence: Whether to return prediction confidence
            
        Returns:
            Predicted costs (and optionally confidence intervals)
        """
        if self.cost_model is None:
            raise ValueError("Cost model not loaded")
        
        # Preprocess
        X_processed = self.preprocess_input(X)
        
        # Predict
        predictions = self.cost_model.predict(X_processed)
        
        if return_confidence and hasattr(self.cost_model, 'estimators_'):
            # For Random Forest, calculate std from trees
            tree_predictions = np.array([
                tree.predict(X_processed) 
                for tree in self.cost_model.estimators_
            ])
            confidence = tree_predictions.std(axis=0)
            return predictions, confidence
        
        return predictions
    
    def predict_co2(
        self,
        X: Union[pd.DataFrame, Dict, List[Dict]],
        return_confidence: bool = False
    ) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
        """
        Predict CO₂ emissions per kg
        
        Args:
            X: Input features
            return_confidence: Whether to return prediction confidence
            
        Returns:
            Predicted CO₂ emissions (and optionally confidence intervals)
        """
        if self.co2_model is None:
            raise ValueError("CO₂ model not loaded")
        
        # Preprocess
        X_processed = self.preprocess_input(X)
        
        # Predict
        predictions = self.co2_model.predict(X_processed)
        
        if return_confidence:
            # For XGBoost, we can't easily get confidence
            # Return predictions with None for confidence
            return predictions, None
        
        return predictions
    
    def predict_all(
        self,
        X: Union[pd.DataFrame, Dict, List[Dict]],
        return_confidence: bool = False
    ) -> pd.DataFrame:
        """
        Predict both cost and CO₂ emissions
        
        Args:
            X: Input features
            return_confidence: Whether to include confidence intervals
            
        Returns:
            DataFrame with predictions
        """
        # Preprocess once
        X_processed = self.preprocess_input(X)
        
        # Predict cost
        if self.cost_model:
            if return_confidence:
                cost_pred, cost_conf = self.predict_cost(X_processed, return_confidence=True)
            else:
                cost_pred = self.predict_cost(X_processed)
                cost_conf = None
        else:
            cost_pred = None
            cost_conf = None
        
        # Predict CO₂
        if self.co2_model:
            if return_confidence:
                co2_pred, co2_conf = self.predict_co2(X_processed, return_confidence=True)
            else:
                co2_pred = self.predict_co2(X_processed)
                co2_conf = None
        else:
            co2_pred = None
            co2_conf = None
        
        # Create results DataFrame
        results = X_processed.copy()
        
        if cost_pred is not None:
            results['predicted_cost'] = cost_pred
            if cost_conf is not None:
                results['cost_confidence'] = cost_conf
        
        if co2_pred is not None:
            results['predicted_co2'] = co2_pred
            if co2_conf is not None:
                results['co2_confidence'] = co2_conf
        
        return results
    
    def predict_single(
        self,
        features: Dict,
        include_confidence: bool = False
    ) -> Dict:
        """
        Predict for a single instance
        
        Args:
            features: Dictionary of feature values
            include_confidence: Whether to include confidence
            
        Returns:
            Dictionary with predictions
        """
        # Convert to DataFrame
        df = pd.DataFrame([features])
        
        # Get predictions
        results_df = self.predict_all(df, return_confidence=include_confidence)
        
        # Convert to dict
        result = results_df.iloc[0].to_dict()
        
        return result
    
    def batch_predict(
        self,
        input_path: str,
        output_path: str,
        include_confidence: bool = False
    ):
        """
        Batch prediction from CSV file
        
        Args:
            input_path: Path to input CSV
            output_path: Path to output CSV
            include_confidence: Whether to include confidence
        """
        logger.info(f"Loading data from {input_path}...")
        df = pd.read_csv(input_path)
        
        logger.info(f"Predicting for {len(df)} instances...")
        results = self.predict_all(df, return_confidence=include_confidence)
        
        logger.info(f"Saving results to {output_path}...")
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        results.to_csv(output_path, index=False)
        
        logger.info("✓ Batch prediction complete")
    
    def get_model_info(self) -> Dict:
        """
        Get information about loaded models
        
        Returns:
            Dictionary with model information
        """
        info = {
            "cost_model": {
                "loaded": self.cost_model is not None,
                "path": self.cost_model_path,
                "type": type(self.cost_model).__name__ if self.cost_model else None
            },
            "co2_model": {
                "loaded": self.co2_model is not None,
                "path": self.co2_model_path,
                "type": type(self.co2_model).__name__ if self.co2_model else None
            },
            "metadata": self.metadata
        }
        
        return info
    
    def validate_predictions(
        self,
        X: pd.DataFrame,
        y_cost: Optional[pd.Series] = None,
        y_co2: Optional[pd.Series] = None
    ) -> Dict:
        """
        Validate predictions against ground truth
        
        Args:
            X: Input features
            y_cost: True cost values
            y_co2: True CO₂ values
            
        Returns:
            Dictionary with validation metrics
        """
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        results = {}
        
        # Predict
        predictions = self.predict_all(X)
        
        # Validate cost
        if y_cost is not None and 'predicted_cost' in predictions.columns:
            cost_pred = predictions['predicted_cost']
            
            results['cost'] = {
                'mae': mean_absolute_error(y_cost, cost_pred),
                'rmse': mean_squared_error(y_cost, cost_pred, squared=False),
                'r2': r2_score(y_cost, cost_pred)
            }
            
            logger.info(f"Cost Model - MAE: {results['cost']['mae']:.4f}, "
                       f"RMSE: {results['cost']['rmse']:.4f}, "
                       f"R²: {results['cost']['r2']:.4f}")
        
        # Validate CO₂
        if y_co2 is not None and 'predicted_co2' in predictions.columns:
            co2_pred = predictions['predicted_co2']
            
            results['co2'] = {
                'mae': mean_absolute_error(y_co2, co2_pred),
                'rmse': mean_squared_error(y_co2, co2_pred, squared=False),
                'r2': r2_score(y_co2, co2_pred)
            }
            
            logger.info(f"CO₂ Model - MAE: {results['co2']['mae']:.4f}, "
                       f"RMSE: {results['co2']['rmse']:.4f}, "
                       f"R²: {results['co2']['r2']:.4f}")
        
        return results


def main():
    """Example usage"""
    # Initialize predictor
    predictor = EcoPackPredictor()
    
    # Example single prediction
    sample_features = {
        'recyclability_percent': 85.0,
        'recycled_content_percent': 60.0,
        'reusability_percent': 40.0,
        'biodegradation_time_days': 180,
        'end_of_life_disposal_percent': 90.0,
        'carbon_footprint_kg_co2_unit': 2.5,
        'waste_reduction_impact_percent': 70.0,
        'sustainability_target_progress_percent': 75.0,
        'load_handling_score': 7.0,
        'moisture_resistance_score': 6.0,
        'thermal_resistance_score': 6.0,
        'annual_usage_units': 10000,
        'total_material_weight_tons': 5.0,
        'supplier_sustainability_compliance_percent': 85.0,
        'co2_impact_index': 0.3,
        'cost_efficiency_index': 0.7,
        'material_suitability_score': 65.0,
        'overall_sustainability_score': 0.75
    }
    
    print("\n" + "="*60)
    print("  EcoPackAI Unified Predictor - Example")
    print("="*60 + "\n")
    
    # Single prediction
    result = predictor.predict_single(sample_features, include_confidence=True)
    
    print("Sample Prediction:")
    print(f"  Predicted Cost: ${result.get('predicted_cost', 'N/A'):.2f}")
    print(f"  Predicted CO₂: {result.get('predicted_co2', 'N/A'):.4f} kg")
    
    if 'cost_confidence' in result and result['cost_confidence']:
        print(f"  Cost Confidence (±): ${result['cost_confidence']:.2f}")
    
    # Model info
    print("\nModel Information:")
    info = predictor.get_model_info()
    for model_type, model_info in info.items():
        if model_type != 'metadata':
            print(f"  {model_type}:")
            print(f"    Loaded: {model_info['loaded']}")
            print(f"    Type: {model_info['type']}")


if __name__ == '__main__':
    main()
