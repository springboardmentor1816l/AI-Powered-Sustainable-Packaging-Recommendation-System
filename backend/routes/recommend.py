"""
Recommendation Route
====================

Flask Blueprint for material recommendation endpoints.
Integrates MaterialRanker with prediction API to provide ranked recommendations.
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import pandas as pd
import numpy as np
from typing import Dict, List, Optional

# Import ranker
try:
    from src.recommendation.ranker import MaterialRanker
    RANKER_AVAILABLE = True
except ImportError as e:
    logging.warning(f"MaterialRanker not available: {e}")
    RANKER_AVAILABLE = False

# Import predictor
try:
    from src.inference.predictor import EcoPackPredictor
    PREDICTOR_AVAILABLE = True
except ImportError as e:
    logging.warning(f"EcoPackPredictor not available: {e}")
    PREDICTOR_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
recommend_bp = Blueprint('recommend', __name__, url_prefix='/api/v1/recommend')

# Global instances (lazy loading)
_ranker = None
_predictor = None


def get_ranker():
    """Get or create MaterialRanker instance (singleton pattern)"""
    global _ranker
    if _ranker is None:
        if not RANKER_AVAILABLE:
            raise RuntimeError("MaterialRanker is not available")
        _ranker = MaterialRanker(ranking_mode='balanced')
        logger.info("MaterialRanker initialized")
    return _ranker


def get_predictor():
    """Get or create EcoPackPredictor instance (singleton pattern)"""
    global _predictor
    if _predictor is None:
        if not PREDICTOR_AVAILABLE:
            raise RuntimeError("EcoPackPredictor is not available")
        _predictor = EcoPackPredictor()
        logger.info("EcoPackPredictor initialized")
    return _predictor


# Required features for prediction
REQUIRED_FEATURES = [
    'recyclability_percent',
    'recycled_content_percent',
    'reusability_percent',
    'biodegradation_time_days',
    'end_of_life_disposal_percent',
    'carbon_footprint_kg_co2_unit',
    'waste_reduction_impact_percent',
    'sustainability_target_progress_percent',
    'load_handling_score',
    'moisture_resistance_score',
    'thermal_resistance_score',
    'annual_usage_units',
    'total_material_weight_tons',
    'supplier_sustainability_compliance_percent',
    'co2_impact_index',
    'cost_efficiency_index',
    'material_suitability_score',
    'overall_sustainability_score'
]


@recommend_bp.route('/', methods=['POST'])
def get_recommendations():
    """
    Get ranked sustainable packaging material recommendations
    
    Request Body:
    {
        "product_data": {
            "recyclability_percent": 95.0,
            "recycled_content_percent": 70.0,
            ... (all 18 features)
        },
        "ranking_mode": "balanced",  // optional: balanced, cost_focused, eco_focused
        "top_n": 5  // optional: number of recommendations to return
    }
    
    Response:
    {
        "status": "success",
        "timestamp": "2026-01-07T19:45:00",
        "ranking_mode": "balanced",
        "recommendations": [
            {
                "rank": 1,
                "material_name": "Recycled Cardboard",
                "predicted_cost": 12.45,
                "predicted_co2": 1.234,
                "sustainability_score": 0.85,
                "ranking_score": 0.92,
                "cost_confidence": 0.87,
                "explanation": "..."
            },
            ...
        ],
        "input_data": {...}
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'No JSON data provided',
                'status': 'error'
            }), 400
        
        # Extract parameters
        product_data = data.get('product_data', {})
        ranking_mode = data.get('ranking_mode', 'balanced')
        top_n = data.get('top_n', 5)
        include_explanations = data.get('include_explanations', True)
        
        # Validate product_data
        if not product_data:
            return jsonify({
                'error': 'product_data is required',
                'status': 'error'
            }), 400
        
        # Validate required features
        missing_features = [f for f in REQUIRED_FEATURES if f not in product_data]
        if missing_features:
            return jsonify({
                'error': f'Missing required features: {", ".join(missing_features[:3])}...',
                'missing_features': missing_features,
                'status': 'error'
            }), 400
        
        # Validate ranking_mode
        valid_modes = ['balanced', 'cost_focused', 'eco_focused']
        if ranking_mode not in valid_modes:
            return jsonify({
                'error': f'Invalid ranking_mode. Must be one of: {", ".join(valid_modes)}',
                'status': 'error'
            }), 400
        
        logger.info(f"Received recommendation request with ranking_mode={ranking_mode}, top_n={top_n}")
        
        # Get predictions from ML models
        predictor = get_predictor()
        
        # Predict cost
        cost_pred = predictor.predict_cost(product_data)
        predicted_cost = cost_pred['predicted_cost']
        cost_confidence = cost_pred['confidence']
        
        # Predict CO2
        co2_pred = predictor.predict_co2(product_data)
        predicted_co2 = co2_pred['predicted_co2']
        
        logger.info(f"Predictions: cost=${predicted_cost:.2f}, co2={predicted_co2:.4f}")
        
        # Generate material recommendations based on the product data
        # For demonstration, we'll create variant materials with slight modifications
        materials = generate_material_variants(
            product_data,
            predicted_cost,
            predicted_co2,
            num_variants=10
        )
        
        # Create DataFrame for ranking
        df = pd.DataFrame(materials)
        
        # Rank materials using MaterialRanker
        ranker = get_ranker()
        
        # Update ranker mode if different
        if ranking_mode != ranker.config.ranking_mode:
            ranker = MaterialRanker(ranking_mode=ranking_mode)
        
        # Apply ranking pipeline
        df_ranked = ranker.rank_materials(df)
        
        # Get top N recommendations
        df_top = ranker.get_top_recommendations(df_ranked, top_n=top_n)
        
        # Convert to recommendation format
        recommendations = []
        for _, row in df_top.iterrows():
            rec = {
                'rank': int(row.get('rank', 0)),
                'material_name': row.get('material_name', 'Unknown Material'),
                'predicted_cost': float(row.get('predicted_cost', predicted_cost)),
                'predicted_co2': float(row.get('predicted_co2', predicted_co2)),
                'sustainability_score': float(row.get('overall_sustainability_score', product_data.get('overall_sustainability_score', 0.0))),
                'ranking_score': float(row.get('ranking_score', 0.0)),
                'cost_confidence': float(row.get('cost_confidence', cost_confidence)),
                'cost_efficiency_index': float(row.get('cost_efficiency_index', product_data.get('cost_efficiency_index', 0.0))),
                'co2_impact_index': float(row.get('co2_impact_index', product_data.get('co2_impact_index', 0.0))),
                'material_suitability_score': float(row.get('material_suitability_score', product_data.get('material_suitability_score', 0.0)))
            }
            
            # Add explanation if requested
            if include_explanations:
                rec['explanation'] = ranker.generate_explanation(row)
            
            recommendations.append(rec)
        
        # Build response
        response = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'ranking_mode': ranking_mode,
            'top_n': top_n,
            'total_evaluated': len(df),
            'recommendations': recommendations,
            'input_data_summary': {
                'recyclability_percent': product_data.get('recyclability_percent'),
                'cost_efficiency_index': product_data.get('cost_efficiency_index'),
                'overall_sustainability_score': product_data.get('overall_sustainability_score')
            }
        }
        
        logger.info(f"Successfully generated {len(recommendations)} recommendations")
        
        return jsonify(response), 200
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 400
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}", exc_info=True)
        return jsonify({
            'error': 'Internal server error while generating recommendations',
            'details': str(e),
            'status': 'error'
        }), 500


def generate_material_variants(base_data: Dict, base_cost: float, base_co2: float, num_variants: int = 10) -> List[Dict]:
    """
    Generate material variants based on base product data
    
    This creates hypothetical material options by varying key parameters
    to demonstrate the ranking system.
    
    Args:
        base_data: Base product data
        base_cost: Base predicted cost
        base_co2: Base predicted CO2
        num_variants: Number of variants to generate
    
    Returns:
        List of material dictionaries
    """
    materials = []
    
    # Define material types with characteristics
    material_types = [
        {"name": "Recycled Cardboard", "cost_mult": 0.8, "co2_mult": 0.7, "sus_mult": 1.2},
        {"name": "Biodegradable Plastic (PLA)", "cost_mult": 1.2, "co2_mult": 0.9, "sus_mult": 1.1},
        {"name": "Virgin Cardboard", "cost_mult": 1.0, "co2_mult": 1.0, "sus_mult": 1.0},
        {"name": "Recycled Paper Pulp", "cost_mult": 0.7, "co2_mult": 0.6, "sus_mult": 1.3},
        {"name": "Molded Fiber", "cost_mult": 0.9, "co2_mult": 0.8, "sus_mult": 1.15},
        {"name": "Mushroom Packaging", "cost_mult": 1.3, "co2_mult": 0.5, "sus_mult": 1.4},
        {"name": "Cornstarch Foam", "cost_mult": 1.1, "co2_mult": 0.85, "sus_mult": 1.2},
        {"name": "Recycled PET", "cost_mult": 1.0, "co2_mult": 1.1, "sus_mult": 1.0},
        {"name": "Wheat Straw Fiber", "cost_mult": 0.95, "co2_mult": 0.75, "sus_mult": 1.25},
        {"name": "Bamboo Fiber", "cost_mult": 1.15, "co2_mult": 0.7, "sus_mult": 1.3}
    ]
    
    for i, mat_type in enumerate(material_types[:num_variants]):
        # Create variant by modifying base data
        material = base_data.copy()
        
        # Update material-specific attributes
        material['material_name'] = mat_type['name']
        material['material_id'] = i + 1
        
        # Adjust cost and CO2 based on material type
        material['predicted_cost'] = base_cost * mat_type['cost_mult'] * np.random.uniform(0.95, 1.05)
        material['predicted_co2'] = base_co2 * mat_type['co2_mult'] * np.random.uniform(0.95, 1.05)
        material['cost_confidence'] = np.random.uniform(0.75, 0.95)
        
        # Adjust sustainability metrics
        material['overall_sustainability_score'] = min(1.0, base_data.get('overall_sustainability_score', 0.8) * mat_type['sus_mult'] * np.random.uniform(0.98, 1.02))
        material['cost_efficiency_index'] = min(1.0, base_data.get('cost_efficiency_index', 0.7) / mat_type['cost_mult'] * np.random.uniform(0.95, 1.05))
        material['co2_impact_index'] = min(1.0, base_data.get('co2_impact_index', 0.3) * mat_type['co2_mult'] * np.random.uniform(0.95, 1.05))
        
        # Slight variations in other metrics
        material['recyclability_percent'] = min(100, base_data.get('recyclability_percent', 80) * np.random.uniform(0.9, 1.1))
        material['recycled_content_percent'] = min(100, base_data.get('recycled_content_percent', 70) * np.random.uniform(0.85, 1.15))
        
        materials.append(material)
    
    return materials


@recommend_bp.route('/modes', methods=['GET'])
def get_ranking_modes():
    """
    Get available ranking modes
    
    Response:
    {
        "modes": [
            {
                "name": "balanced",
                "description": "Balanced weighting of cost and sustainability",
                "weights": {...}
            },
            ...
        ]
    }
    """
    modes = [
        {
            "name": "balanced",
            "description": "Balanced weighting of cost and sustainability",
            "weights": {
                "cost": 0.35,
                "co2": 0.35,
                "sustainability": 0.30
            }
        },
        {
            "name": "cost_focused",
            "description": "Prioritizes lower costs with minimum sustainability requirements",
            "weights": {
                "cost": 0.60,
                "co2": 0.20,
                "sustainability": 0.20
            }
        },
        {
            "name": "eco_focused",
            "description": "Maximizes environmental sustainability",
            "weights": {
                "cost": 0.20,
                "co2": 0.40,
                "sustainability": 0.40
            }
        }
    ]
    
    return jsonify({
        "status": "success",
        "modes": modes
    }), 200


@recommend_bp.route('/health', methods=['GET'])
def health():
    """Health check for recommendation service"""
    try:
        ranker_status = "available" if RANKER_AVAILABLE else "unavailable"
        predictor_status = "available" if PREDICTOR_AVAILABLE else "unavailable"
        
        return jsonify({
            "status": "healthy" if (RANKER_AVAILABLE and PREDICTOR_AVAILABLE) else "degraded",
            "ranker": ranker_status,
            "predictor": predictor_status,
            "timestamp": datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 503


# Export blueprint
__all__ = ['recommend_bp']
