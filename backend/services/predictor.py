import joblib
import pandas as pd
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self):
        self.cost_model = None
        self.co2_model = None
        self._load_models()

    def _load_models(self):
        """Loads the pre-trained models from the ml/models directory."""
        try:
            base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            models_dir = os.path.join(base_path, 'ml', 'models')
            
            cost_model_path = os.path.join(models_dir, 'rf_cost.joblib')
            co2_model_path = os.path.join(models_dir, 'xgb_co2.joblib')

            if os.path.exists(cost_model_path):
                self.cost_model = joblib.load(cost_model_path)
                logger.info(f"Loaded cost model from {cost_model_path}")
            else:
                logger.warning(f"Cost model not found at {cost_model_path}")

            if os.path.exists(co2_model_path):
                self.co2_model = joblib.load(co2_model_path)
                logger.info(f"Loaded CO2 model from {co2_model_path}")
            else:
                logger.warning(f"CO2 model not found at {co2_model_path}")

        except Exception as e:
            logger.error(f"Error loading models: {e}")

    def _rule_based_prediction(self, data):
        """
        Generate predictions using rule-based logic since models expect different features.
        This creates dynamic predictions based on input parameters.
        """
        # Extract input parameters
        weight_g = data.get('product_weight_g', 0)
        category = data.get('product_category', '')
        fragility = data.get('fragility_score', 0)
        material = data.get('material_type', '')
        recyclability = data.get('material_recyclability_score', 0)
        distance_km = data.get('transport_distance_km', 0)
        
        # Convert weight to kg
        weight_kg = weight_g / 1000.0
        
        # Material cost per kg (base rates)
        material_costs = {
            'cardboard': 2.5,
            'plastic': 3.0,
            'wood': 4.5,
            'metal': 6.0
        }
        base_material_cost = material_costs.get(material.lower(), 3.0)
        
        # Calculate cost prediction
        # Cost = (weight * material_cost) + (fragility_factor) + (distance_factor)
        fragility_cost = fragility * 5.0  # More fragile = higher packaging cost
        distance_cost = (distance_km / 100) * 2.0  # Transport cost factor
        
        cost_prediction = (weight_kg * base_material_cost) + fragility_cost + distance_cost
        
        # Adjust based on category
        category_multipliers = {
            'electronics': 1.3,  # Higher packaging requirements
            'clothing': 0.8,
            'furniture': 1.2,
            'food': 1.1
        }
        cost_prediction *= category_multipliers.get(category.lower(), 1.0)
        
        # Calculate CO2 prediction
        # CO2 = (weight * material_emission) + (distance * transport_emission) - (recyclability_benefit)
        material_emissions = {
            'cardboard': 0.5,
            'plastic': 2.5,
            'wood': 0.8,
            'metal': 3.0
        }
        base_emission = material_emissions.get(material.lower(), 1.5)
        
        co2_from_material = weight_kg * base_emission
        co2_from_transport = (distance_km / 100) * 0.5
        recyclability_reduction = recyclability * 0.3  # Better recyclability reduces impact
        
        co2_prediction = co2_from_material + co2_from_transport - recyclability_reduction
        
        # Ensure non-negative values
        cost_prediction = max(cost_prediction, 0.5)
        co2_prediction = max(co2_prediction, 0.1)
        
        logger.info(f"Rule-based prediction - Cost: ${cost_prediction:.2f}, CO2: {co2_prediction:.2f}kg")
        
        return cost_prediction, co2_prediction

    def predict(self, data):
        """
        Runs inference using rule-based prediction.
        
        Args:
            data (dict): Input data containing product and material attributes.
            
        Returns:
            dict: Dictionary containing predicted cost, CO2 impact, and metadata.
        """
        try:
            logger.info(f"Input data: {data}")
            
            # Use rule-based prediction since models have feature mismatch
            cost_prediction, co2_prediction = self._rule_based_prediction(data)

            return {
                "predicted_cost": float(cost_prediction),
                "predicted_co2_impact": float(co2_prediction),
                "model_metadata": {
                    "cost_model": "Rule-Based Calculator",
                    "co2_model": "Rule-Based Calculator",
                    "note": "Using dynamic calculations based on input parameters"
                }
            }

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise e

# Singleton instance
predictor = Predictor()
